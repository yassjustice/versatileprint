"""
Order management service.
Handles order creation, updates, and status transitions with quota enforcement.
"""
from datetime import datetime, date
from typing import Tuple, Optional, List, Dict, Any
from flask import current_app

from app.models.order import Order, OrderStatus
from app.models.user import User
from app.models.audit_log import AuditLog
from app.services.quota_service import QuotaService
from app.utils.helpers import get_current_month


class OrderService:
    """Order management service."""
    
    @staticmethod
    def create_order(client_id: int, bw_quantity: int, color_quantity: int,
                     paper_dimensions: str = None, paper_type: str = None,
                     finishing: str = None, notes: str = None,
                     agent_id: int = None, external_order_id: str = None,
                     import_id: int = None, created_by_id: int = None) -> Tuple[bool, Optional[Order], Optional[str]]:
        """
        Create a new order with quota enforcement.
        
        Args:
            client_id: Client user ID
            bw_quantity: B&W prints quantity
            color_quantity: Color prints quantity
            paper_dimensions: Paper size (e.g., A4)
            paper_type: Paper type (e.g., matte, glossy)
            finishing: Finishing option (e.g., staple, bind)
            notes: Optional notes
            agent_id: Optional agent ID (if created by agent)
            external_order_id: External ID for idempotency
            import_id: CSV import ID (if from CSV)
            created_by_id: User ID creating the order (for audit)
        
        Returns:
            (success, order, error_message)
        """
        try:
            # Validate client exists and is active
            client = User.get_by_id(client_id)
            if not client or not client.is_client:
                return False, None, 'Invalid client ID'
            
            if not client.is_active:
                return False, None, 'Client account is not active'
            
            # Check for duplicate external_order_id
            if external_order_id:
                existing = Order.get_by_external_id(external_order_id)
                if existing:
                    idempotency_mode = current_app.config.get('CSV_IDEMPOTENCY_MODE', 'reject')
                    if idempotency_mode == 'reject':
                        return False, None, f'Duplicate order: external_order_id "{external_order_id}" already exists'
                    elif idempotency_mode == 'skip':
                        return True, existing, None  # Return existing order
            
            # Validate agent if provided
            if agent_id:
                agent = User.get_by_id(agent_id)
                if not agent or not agent.is_agent:
                    return False, None, 'Invalid agent ID'
                
                if not agent.is_active:
                    return False, None, 'Agent account is not active'
                
                # Check agent workload limit
                max_limit = current_app.config.get('MAX_ACTIVE_ORDERS_DEFAULT', 10)
                if not agent.can_accept_order(max_limit):
                    active_count = agent.get_active_orders_count()
                    return False, None, f'Agent workload limit exceeded. Active orders: {active_count}/{max_limit}'
            
            # Check quota availability (server-side enforcement)
            current_month = get_current_month()
            can_fulfill, quota_error, available_quota = QuotaService.check_quota_available(
                client_id, bw_quantity, color_quantity, current_month
            )
            
            if not can_fulfill:
                return False, None, quota_error
            
            # Create order
            order = Order(
                client_id=client_id,
                agent_id=agent_id,
                bw_quantity=bw_quantity,
                color_quantity=color_quantity,
                paper_dimensions=paper_dimensions,
                paper_type=paper_type,
                finishing=finishing,
                notes=notes,
                external_order_id=external_order_id,
                import_id=import_id,
                status=OrderStatus.PENDING
            )
            order.save()
            
            # Deduct quota with transaction safety
            deduct_success, deduct_error = QuotaService.deduct_quota(
                client_id, bw_quantity, color_quantity, current_month
            )
            
            if not deduct_success:
                # Rollback order creation
                order.delete()
                return False, None, f'Failed to deduct quota: {deduct_error}'
            
            # Log creation
            AuditLog.log_action(
                action='ORDER_CREATED',
                user_id=created_by_id or client_id,
                details={
                    'order_id': order.id,
                    'client_id': client_id,
                    'agent_id': agent_id,
                    'bw_quantity': bw_quantity,
                    'color_quantity': color_quantity,
                    'import_id': import_id
                }
            )
            
            # Send notification to client
            from app.services.notification_service import NotificationService
            NotificationService.create_order_notification(order.id, client_id, 'created')
            
            # Notify agent if assigned
            if agent_id:
                NotificationService.create_order_notification(order.id, agent_id, 'assigned')
            
            return True, order, None
            
        except Exception as e:
            return False, None, f'Failed to create order: {str(e)}'
    
    @staticmethod
    def change_order_status(order_id: int, new_status: str, changed_by_id: int) -> Tuple[bool, Optional[str]]:
        """
        Change order status with validation and notifications.
        
        Args:
            order_id: Order ID
            new_status: New status value
            changed_by_id: User ID making the change
        
        Returns:
            (success, error_message)
        """
        try:
            # Get order
            order = Order.get_by_id(order_id)
            if not order:
                return False, 'Order not found'
            
            # Validate transition
            old_status = order.status_value
            
            # Attempt status change
            success = order.change_status(new_status, changed_by_id)
            
            if not success:
                allowed_transitions = {
                    'pending': ['validated'],
                    'validated': ['processing'],
                    'processing': ['completed'],
                    'completed': []
                }
                allowed = allowed_transitions.get(old_status, [])
                return False, f'Invalid status transition from "{old_status}" to "{new_status}". Allowed: {", ".join(allowed) if allowed else "none"}'
            
            # Send notifications
            from app.services.notification_service import NotificationService
            NotificationService.create_status_change_notification(order, old_status, new_status)
            
            return True, None
            
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_orders_for_user(user: User, status: str = None, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """
        Get orders for user based on role.
        
        Args:
            user: User object
            status: Optional status filter
            page: Page number
            page_size: Items per page
        
        Returns:
            Paginated orders dictionary
        """
        from app.utils.helpers import paginate_query_results
        
        # Get orders based on role
        if user.is_admin:
            # Admins see all orders
            session = user.get_session()
            query = session.query(Order)
            
            if status:
                query = query.filter_by(status=OrderStatus(status))
            
            query = query.order_by(Order.created_at.desc())
            orders = query.all()
            
        elif user.is_agent:
            # Agents see their assigned orders
            orders = Order.get_by_agent(user.id, status)
            
        elif user.is_client:
            # Clients see their own orders
            orders = Order.get_by_client(user.id, status)
            
        else:
            orders = []
        
        # Convert to dict
        orders_data = [order.to_dict(include_relations=True) for order in orders]
        
        # Paginate
        return paginate_query_results(orders_data, page, page_size)
    
    @staticmethod
    def get_order_details(order_id: int, user: User) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Get order details with authorization check.
        
        Args:
            order_id: Order ID
            user: Requesting user
        
        Returns:
            (success, order_dict, error_message)
        """
        order = Order.get_by_id(order_id)
        
        if not order:
            return False, None, 'Order not found'
        
        # Authorization check
        if not user.is_admin:
            if user.is_client and order.client_id != user.id:
                return False, None, 'Access forbidden'
            elif user.is_agent and order.agent_id != user.id:
                return False, None, 'Access forbidden'
        
        return True, order.to_dict(include_relations=True), None
    
    @staticmethod
    def get_orders_by_month(client_id: int, month: date) -> List[Order]:
        """
        Get all orders for a client in a specific month.
        
        Args:
            client_id: Client user ID
            month: Month date
        
        Returns:
            List of orders
        """
        from app.utils.helpers import normalize_month
        
        month_start = normalize_month(month)
        
        # Calculate month end
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year + 1, month=1)
        else:
            month_end = month_start.replace(month=month_start.month + 1)
        
        session = Order.get_session()
        orders = session.query(Order).filter(
            Order.client_id == client_id,
            Order.created_at >= month_start,
            Order.created_at < month_end
        ).all()
        
        return orders
    
    @staticmethod
    def get_statistics(month: date = None) -> Dict[str, Any]:
        """
        Get order statistics for reporting.
        
        Args:
            month: Optional month filter
        
        Returns:
            Statistics dictionary
        """
        session = Order.get_session()
        query = session.query(Order)
        
        if month:
            from app.utils.helpers import normalize_month
            month_start = normalize_month(month)
            
            if month_start.month == 12:
                month_end = month_start.replace(year=month_start.year + 1, month=1)
            else:
                month_end = month_start.replace(month=month_start.month + 1)
            
            query = query.filter(
                Order.created_at >= month_start,
                Order.created_at < month_end
            )
        
        orders = query.all()
        
        # Calculate statistics
        stats = {
            'total_orders': len(orders),
            'by_status': {},
            'total_bw': sum(o.bw_quantity for o in orders),
            'total_color': sum(o.color_quantity for o in orders)
        }
        
        # Count by status
        for status in OrderStatus:
            count = sum(1 for o in orders if o.status == status)
            stats['by_status'][status.value] = count
        
        return stats
