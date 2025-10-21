"""
Quota management service.
Handles quota enforcement, top-ups, and usage tracking with transaction safety.
"""
from datetime import date, datetime
from typing import Tuple, Optional, Dict, Any
from flask import current_app
from sqlalchemy import text

from app.models.quota import ClientQuota, QuotaTopup
from app.models.user import User
from app.models.audit_log import AuditLog
from app.utils.helpers import normalize_month, get_current_month, format_quota_message


class QuotaService:
    """Quota management service with transaction-safe operations."""
    
    @staticmethod
    def get_or_create_quota(client_id: int, month: date = None) -> ClientQuota:
        """
        Get existing quota or create new one for month.
        
        Args:
            client_id: Client user ID
            month: Month date (defaults to current month)
        
        Returns:
            ClientQuota instance
        """
        if month is None:
            month = get_current_month()
        else:
            month = normalize_month(month)
        
        # Get default limits from config
        bw_limit = current_app.config.get('DEFAULT_BW_LIMIT', 3000)
        color_limit = current_app.config.get('DEFAULT_COLOR_LIMIT', 2000)
        
        return ClientQuota.get_or_create(client_id, month, bw_limit, color_limit)
    
    @staticmethod
    def check_quota_available(client_id: int, bw_quantity: int, color_quantity: int, month: date = None) -> Tuple[bool, Optional[str], Optional[Dict[str, int]]]:
        """
        Check if quota is available for order (server-side enforcement).
        
        Args:
            client_id: Client user ID
            bw_quantity: B&W quantity requested
            color_quantity: Color quantity requested
            month: Month to check (defaults to current month)
        
        Returns:
            (can_fulfill, error_message, available_quota_dict)
        """
        # Get or create quota
        quota = QuotaService.get_or_create_quota(client_id, month)
        
        # Check if can fulfill
        can_fulfill, message = quota.can_fulfill(bw_quantity, color_quantity)
        
        if not can_fulfill:
            # Format detailed error message
            total_bw, total_color = quota.get_total_limits()
            
            if bw_quantity > quota.get_available_bw():
                message = format_quota_message(
                    'B&W',
                    quota.get_available_bw(),
                    total_bw,
                    bw_quantity
                )
            elif color_quantity > quota.get_available_color():
                message = format_quota_message(
                    'Color',
                    quota.get_available_color(),
                    total_color,
                    color_quantity
                )
            
            return False, message, None
        
        # Return available quota details
        available = {
            'bw_available': quota.get_available_bw(),
            'color_available': quota.get_available_color(),
            'bw_used': quota.bw_used,
            'color_used': quota.color_used
        }
        
        return True, None, available
    
    @staticmethod
    def deduct_quota(client_id: int, bw_quantity: int, color_quantity: int, month: date = None) -> Tuple[bool, Optional[str]]:
        """
        Deduct quota with transaction safety (row-level locking).
        
        Args:
            client_id: Client user ID
            bw_quantity: B&W quantity to deduct
            color_quantity: Color quantity to deduct
            month: Month to deduct from (defaults to current month)
        
        Returns:
            (success, error_message)
        """
        if month is None:
            month = get_current_month()
        else:
            month = normalize_month(month)
        
        try:
            session = current_app.db_session
            
            # Begin transaction with row-level lock (SELECT ... FOR UPDATE)
            quota = session.query(ClientQuota).filter_by(
                client_id=client_id,
                month=month
            ).with_for_update().first()
            
            if not quota:
                # Create quota if doesn't exist
                quota = QuotaService.get_or_create_quota(client_id, month)
                # Re-lock it
                session.refresh(quota, with_for_update=True)
            
            # Double-check availability under lock
            can_fulfill, error_msg = quota.can_fulfill(bw_quantity, color_quantity)
            if not can_fulfill:
                session.rollback()
                return False, error_msg
            
            # Deduct quota
            quota.bw_used += bw_quantity
            quota.color_used += color_quantity
            
            # Check for quota alerts
            threshold = current_app.config.get('QUOTA_WARNING_THRESHOLD', 0.8)
            alert_status = quota.check_usage_threshold(threshold)
            
            session.commit()
            
            # Send alerts if thresholds exceeded (outside transaction)
            if alert_status['bw_exceeded']:
                QuotaService._send_quota_alert(client_id, 'bw', quota, threshold)
                quota.mark_alert_sent('bw')
            
            if alert_status['color_exceeded']:
                QuotaService._send_quota_alert(client_id, 'color', quota, threshold)
                quota.mark_alert_sent('color')
            
            return True, None
            
        except Exception as e:
            session.rollback()
            return False, f'Failed to deduct quota: {str(e)}'
    
    @staticmethod
    def refund_quota(client_id: int, bw_quantity: int, color_quantity: int, month: date = None) -> Tuple[bool, Optional[str]]:
        """
        Refund quota (rollback a deduction) - used when order creation fails after quota deduction.
        
        Args:
            client_id: Client user ID
            bw_quantity: B&W quantity to refund
            color_quantity: Color quantity to refund
            month: Month to refund to (defaults to current month)
        
        Returns:
            (success, error_message)
        """
        if month is None:
            month = get_current_month()
        else:
            month = normalize_month(month)
        
        try:
            session = current_app.db_session
            
            # Get quota with lock
            quota = session.query(ClientQuota).filter_by(
                client_id=client_id,
                month=month
            ).with_for_update().first()
            
            if not quota:
                # If quota doesn't exist, nothing to refund
                return True, None
            
            # Refund quota (subtract from used)
            quota.bw_used = max(0, quota.bw_used - bw_quantity)
            quota.color_used = max(0, quota.color_used - color_quantity)
            
            session.commit()
            
            # Log refund
            AuditLog.log_action(
                action='QUOTA_REFUND',
                user_id=client_id,
                details={
                    'client_id': client_id,
                    'bw_refunded': bw_quantity,
                    'color_refunded': color_quantity,
                    'month': month.isoformat(),
                    'reason': 'Order creation failed'
                }
            )
            
            return True, None
            
        except Exception as e:
            session.rollback()
            return False, f'Failed to refund quota: {str(e)}'
    
    @staticmethod
    def create_topup(client_id: int, admin_id: int, bw_added: int = 0, color_added: int = 0, notes: str = None) -> Tuple[bool, Optional[QuotaTopup], Optional[str]]:
        """
        Create quota top-up transaction.
        
        Args:
            client_id: Client user ID
            admin_id: Administrator user ID
            bw_added: B&W quota to add
            color_added: Color quota to add
            notes: Optional notes
        
        Returns:
            (success, topup, error_message)
        """
        # Validate minimum top-up
        min_topup = current_app.config.get('MIN_TOPUP_AMOUNT', 1000)
        
        if bw_added > 0 and bw_added < min_topup:
            return False, None, f'B&W top-up must be at least {min_topup} prints'
        
        if color_added > 0 and color_added < min_topup:
            return False, None, f'Color top-up must be at least {min_topup} prints'
        
        if bw_added == 0 and color_added == 0:
            return False, None, 'Top-up must add at least one type of quota'
        
        try:
            # Create top-up
            topup = QuotaTopup.create_topup(client_id, admin_id, bw_added, color_added, notes)
            
            # Log action
            AuditLog.log_action(
                action='QUOTA_TOPUP',
                user_id=admin_id,
                details={
                    'client_id': client_id,
                    'bw_added': bw_added,
                    'color_added': color_added,
                    'topup_id': topup.id
                }
            )
            
            # Send notification to client
            from app.services.notification_service import NotificationService
            NotificationService.create_topup_notification(client_id, bw_added, color_added)
            
            return True, topup, None
            
        except Exception as e:
            return False, None, str(e)
    
    @staticmethod
    def get_quota_summary(client_id: int, month: date = None) -> Dict[str, Any]:
        """
        Get comprehensive quota summary for client.
        
        Args:
            client_id: Client user ID
            month: Month to get summary for (defaults to current month)
        
        Returns:
            Dictionary with quota details
        """
        quota = QuotaService.get_or_create_quota(client_id, month)
        total_bw, total_color = quota.get_total_limits()
        
        # Get top-ups for month
        topups = QuotaTopup.get_topups_for_month(client_id, quota.month)
        
        summary = {
            'client_id': client_id,
            'month': quota.month.isoformat(),
            'bw': {
                'base_limit': quota.bw_limit,
                'topups': sum(t.bw_added for t in topups),
                'total_limit': total_bw,
                'used': quota.bw_used,
                'available': quota.get_available_bw(),
                'percentage_used': round((quota.bw_used / total_bw * 100) if total_bw > 0 else 0, 2)
            },
            'color': {
                'base_limit': quota.color_limit,
                'topups': sum(t.color_added for t in topups),
                'total_limit': total_color,
                'used': quota.color_used,
                'available': quota.get_available_color(),
                'percentage_used': round((quota.color_used / total_color * 100) if total_color > 0 else 0, 2)
            },
            'topups_history': [t.to_dict() for t in topups]
        }
        
        return summary
    
    @staticmethod
    def _send_quota_alert(client_id: int, quota_type: str, quota: ClientQuota, threshold: float):
        """
        Send quota warning alert (internal method).
        
        Args:
            client_id: Client user ID
            quota_type: 'bw' or 'color'
            quota: ClientQuota instance
            threshold: Warning threshold (e.g., 0.8 for 80%)
        """
        from app.services.notification_service import NotificationService
        
        total_bw, total_color = quota.get_total_limits()
        
        if quota_type == 'bw':
            percentage = (quota.bw_used / total_bw * 100) if total_bw > 0 else 0
            message = (
                f'⚠️ B&W Quota Alert: You have used {percentage:.1f}% ({quota.bw_used}/{total_bw}) '
                f'of your B&W printing quota for {quota.month.strftime("%B %Y")}. '
                f'Consider requesting a top-up to avoid service interruption.'
            )
        else:  # color
            percentage = (quota.color_used / total_color * 100) if total_color > 0 else 0
            message = (
                f'⚠️ Color Quota Alert: You have used {percentage:.1f}% ({quota.color_used}/{total_color}) '
                f'of your Color printing quota for {quota.month.strftime("%B %Y")}. '
                f'Consider requesting a top-up to avoid service interruption.'
            )
        
        # Send in-app notification
        NotificationService.create_notification(
            user_id=client_id,
            message=message,
            notification_type='warning'
        )
        
        # Send email notification
        NotificationService.send_quota_alert_email(client_id, quota_type, percentage, quota.month)
