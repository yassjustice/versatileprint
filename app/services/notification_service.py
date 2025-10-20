"""
Notification service.
Handles in-app and email notifications.
"""
from typing import Optional
from datetime import date
from flask import current_app, render_template_string
from flask_mail import Message

from app import mail
from app.models.notification import Notification
from app.models.user import User
from app.models.order import Order


class NotificationService:
    """Notification service for in-app and email notifications."""
    
    @staticmethod
    def create_notification(user_id: int, message: str, notification_type: str = 'info', 
                           related_order_id: int = None) -> Notification:
        """
        Create an in-app notification.
        
        Args:
            user_id: User ID to notify
            message: Notification message
            notification_type: Type (info, warning, error, success)
            related_order_id: Optional related order ID
        
        Returns:
            Created notification
        """
        return Notification.create_notification(user_id, message, notification_type, related_order_id)
    
    @staticmethod
    def create_order_notification(order_id: int, user_id: int, event_type: str):
        """
        Create order-related notification.
        
        Args:
            order_id: Order ID
            user_id: User ID to notify
            event_type: Event type (created, assigned, etc.)
        """
        order = Order.get_by_id(order_id)
        if not order:
            return
        
        messages = {
            'created': f'✓ Order #{order_id} has been created successfully. B&W: {order.bw_quantity}, Color: {order.color_quantity}',
            'assigned': f'📋 You have been assigned to Order #{order_id}. B&W: {order.bw_quantity}, Color: {order.color_quantity}',
            'updated': f'✏️ Order #{order_id} has been updated.',
        }
        
        message = messages.get(event_type, f'Order #{order_id} event: {event_type}')
        
        NotificationService.create_notification(
            user_id=user_id,
            message=message,
            notification_type='info',
            related_order_id=order_id
        )
        
        # Send email for important events
        if event_type in ['created', 'assigned']:
            NotificationService.send_order_email(user_id, order, event_type)
    
    @staticmethod
    def create_status_change_notification(order: Order, old_status: str, new_status: str):
        """
        Create notifications for order status change.
        
        Args:
            order: Order object
            old_status: Previous status
            new_status: New status
        """
        status_messages = {
            'validated': '✓ Order has been validated and approved',
            'processing': '⚙️ Order is now being processed',
            'completed': '✅ Order has been completed'
        }
        
        message = f'Order #{order.id} status changed: {status_messages.get(new_status, new_status)}'
        
        # Notify client
        NotificationService.create_notification(
            user_id=order.client_id,
            message=message,
            notification_type='success' if new_status == 'completed' else 'info',
            related_order_id=order.id
        )
        
        # Notify agent if assigned
        if order.agent_id:
            NotificationService.create_notification(
                user_id=order.agent_id,
                message=message,
                notification_type='info',
                related_order_id=order.id
            )
        
        # Send email notification
        NotificationService.send_status_change_email(order, old_status, new_status)
    
    @staticmethod
    def create_topup_notification(client_id: int, bw_added: int, color_added: int):
        """
        Create notification for quota top-up.
        
        Args:
            client_id: Client user ID
            bw_added: B&W quota added
            color_added: Color quota added
        """
        parts = []
        if bw_added > 0:
            parts.append(f'{bw_added} B&W prints')
        if color_added > 0:
            parts.append(f'{color_added} Color prints')
        
        message = f'✨ Your quota has been topped up: {" and ".join(parts)}'
        
        NotificationService.create_notification(
            user_id=client_id,
            message=message,
            notification_type='success'
        )
        
        # Send email
        NotificationService.send_topup_email(client_id, bw_added, color_added)
    
    @staticmethod
    def create_csv_notification(admin_id: int, import_id: int, status: str, message: str):
        """
        Create notification for CSV import outcome.
        
        Args:
            admin_id: Admin user ID
            import_id: CSV import ID
            status: Import status
            message: Notification message
        """
        notification_type = 'success' if status == 'validated' else 'error' if status == 'rejected' else 'info'
        
        NotificationService.create_notification(
            user_id=admin_id,
            message=message,
            notification_type=notification_type
        )
        
        # Send email
        NotificationService.send_csv_outcome_email(admin_id, import_id, status, message)
    
    @staticmethod
    def send_order_email(user_id: int, order: Order, event_type: str):
        """Send email for order events."""
        user = User.get_by_id(user_id)
        if not user or not user.email:
            return
        
        subjects = {
            'created': f'Order #{order.id} Created',
            'assigned': f'New Order #{order.id} Assigned to You'
        }
        
        subject = subjects.get(event_type, f'Order #{order.id} Update')
        
        # Simple email template
        body = f"""
        <html>
        <body>
            <h2>{subject}</h2>
            <p>Dear {user.full_name or user.email},</p>
            <p><strong>Order Details:</strong></p>
            <ul>
                <li>Order ID: #{order.id}</li>
                <li>B&W Quantity: {order.bw_quantity}</li>
                <li>Color Quantity: {order.color_quantity}</li>
                <li>Paper: {order.paper_dimensions or 'N/A'} - {order.paper_type or 'N/A'}</li>
                <li>Status: {order.status_value}</li>
            </ul>
            <p>Thank you for using VersatilesPrint.</p>
        </body>
        </html>
        """
        
        NotificationService._send_email(user.email, subject, body)
    
    @staticmethod
    def send_status_change_email(order: Order, old_status: str, new_status: str):
        """Send email for order status change."""
        client = User.get_by_id(order.client_id)
        if not client or not client.email:
            return
        
        subject = f'Order #{order.id} Status Update: {new_status.title()}'
        
        body = f"""
        <html>
        <body>
            <h2>Order Status Update</h2>
            <p>Dear {client.full_name or client.email},</p>
            <p>Your order status has been updated:</p>
            <ul>
                <li>Order ID: #{order.id}</li>
                <li>Previous Status: {old_status.title()}</li>
                <li>New Status: {new_status.title()}</li>
                <li>B&W: {order.bw_quantity}, Color: {order.color_quantity}</li>
            </ul>
            <p>Thank you for using VersatilesPrint.</p>
        </body>
        </html>
        """
        
        NotificationService._send_email(client.email, subject, body)
    
    @staticmethod
    def send_topup_email(client_id: int, bw_added: int, color_added: int):
        """Send email for quota top-up."""
        client = User.get_by_id(client_id)
        if not client or not client.email:
            return
        
        subject = 'Quota Top-Up Confirmation'
        
        parts = []
        if bw_added > 0:
            parts.append(f'{bw_added} B&W prints')
        if color_added > 0:
            parts.append(f'{color_added} Color prints')
        
        body = f"""
        <html>
        <body>
            <h2>Quota Top-Up</h2>
            <p>Dear {client.full_name or client.email},</p>
            <p>Your printing quota has been topped up:</p>
            <ul>
                <li>{" and ".join(parts)}</li>
            </ul>
            <p>Your updated quota is now available for use.</p>
            <p>Thank you for using VersatilesPrint.</p>
        </body>
        </html>
        """
        
        NotificationService._send_email(client.email, subject, body)
    
    @staticmethod
    def send_quota_alert_email(client_id: int, quota_type: str, percentage: float, month: date):
        """Send quota warning alert email."""
        client = User.get_by_id(client_id)
        if not client or not client.email:
            return
        
        quota_name = 'B&W' if quota_type == 'bw' else 'Color'
        subject = f'⚠️ {quota_name} Quota Alert - {percentage:.0f}% Used'
        
        body = f"""
        <html>
        <body>
            <h2>Quota Usage Alert</h2>
            <p>Dear {client.full_name or client.email},</p>
            <p>This is an automated alert to inform you that you have used <strong>{percentage:.1f}%</strong> 
            of your {quota_name} printing quota for {month.strftime('%B %Y')}.</p>
            <p>To avoid service interruption, we recommend:</p>
            <ul>
                <li>Monitoring your remaining quota</li>
                <li>Requesting a quota top-up if needed</li>
            </ul>
            <p>Contact your administrator to request a quota increase.</p>
            <p>Thank you for using VersatilesPrint.</p>
        </body>
        </html>
        """
        
        NotificationService._send_email(client.email, subject, body)
    
    @staticmethod
    def send_csv_outcome_email(admin_id: int, import_id: int, status: str, message: str):
        """Send email for CSV import outcome."""
        admin = User.get_by_id(admin_id)
        if not admin or not admin.email:
            return
        
        subject = f'CSV Import #{import_id} - {status.title()}'
        
        body = f"""
        <html>
        <body>
            <h2>CSV Import Update</h2>
            <p>Dear {admin.full_name or admin.email},</p>
            <p>CSV Import #{import_id} has been {status}.</p>
            <p>{message}</p>
            <p>VersatilesPrint System</p>
        </body>
        </html>
        """
        
        NotificationService._send_email(admin.email, subject, body)
    
    @staticmethod
    def _send_email(to: str, subject: str, html_body: str):
        """
        Send email via Flask-Mail.
        
        Args:
            to: Recipient email
            subject: Email subject
            html_body: HTML email body
        """
        try:
            msg = Message(
                subject=subject,
                recipients=[to],
                html=html_body,
                sender=current_app.config.get('MAIL_DEFAULT_SENDER')
            )
            mail.send(msg)
        except Exception as e:
            # Log error but don't fail the operation
            current_app.logger.error(f'Failed to send email to {to}: {str(e)}')
