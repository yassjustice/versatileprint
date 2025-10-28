"""
Order management API endpoints.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app.models.order import Order
from app.models.user import User
from app.services.order_service import OrderService
from app.utils.decorators import admin_required
from app.utils.helpers import build_error_response, build_success_response
from app.utils.validators import validate_order_data

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('', methods=['GET'])
@login_required
def list_orders():
    """GET /api/orders - List orders (role-filtered)."""
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    status = request.args.get('status')
    
    result = OrderService.get_orders_for_user(current_user, status, page, page_size)
    return jsonify(build_success_response(result)[0]), 200


@orders_bp.route('', methods=['POST'])
@login_required
def create_order():
    """POST /api/orders - Create new order."""
    data = request.get_json()
    
    if not data:
        return jsonify(build_error_response('VALIDATION_ERROR', 'Request body required')[0]), 400
    
    # Set client_id based on role
    if current_user.is_client:
        data['client_id'] = current_user.id
    elif current_user.is_agent and not data.get('client_id'):
        return jsonify(build_error_response('VALIDATION_ERROR', 'Agent must specify client_id')[0]), 400
    
    # Validate data
    valid, validated_data, errors = validate_order_data(data)
    if not valid:
        return jsonify(build_error_response('VALIDATION_ERROR', 'Validation failed', errors)[0]), 400
    
    # Add agent_id if agent creating
    if current_user.is_agent:
        validated_data['agent_id'] = current_user.id
    
    # Create order
    success, order, error = OrderService.create_order(
        **validated_data,
        created_by_id=current_user.id
    )
    
    if not success:
        if 'quota' in error.lower():
            return jsonify(build_error_response('QUOTA_EXCEEDED', error)[0]), 400
        elif 'limit' in error.lower():
            return jsonify(build_error_response('AGENT_LIMIT_EXCEEDED', error)[0]), 400
        return jsonify(build_error_response('VALIDATION_ERROR', error)[0]), 400
    
    return jsonify(build_success_response(order.to_dict(include_relations=True), 'Order created', 201)[0]), 201


@orders_bp.route('/<int:order_id>', methods=['GET'])
@login_required
def get_order(order_id):
    """GET /api/orders/:id - Get order details."""
    success, order_data, error = OrderService.get_order_details(order_id, current_user)
    
    if not success:
        code = 'NOT_FOUND' if 'not found' in error.lower() else 'PERMISSION_DENIED'
        return jsonify(build_error_response(code, error)[0]), 404 if code == 'NOT_FOUND' else 403
    
    return jsonify(build_success_response(order_data)[0]), 200


@orders_bp.route('/<int:order_id>/status', methods=['POST'])
@login_required
def change_status(order_id):
    """POST /api/orders/:id/status - Change order status."""
    try:
        data = request.get_json()
        
        if not data or not data.get('status'):
            return jsonify(build_error_response('VALIDATION_ERROR', 'Status is required')[0]), 400
        
        new_status = data['status']
        
        # Get order to check permissions
        order = Order.get_by_id(order_id)
        if not order:
            return jsonify(build_error_response('NOT_FOUND', 'Order not found')[0]), 404
        
        # Authorization check: Admin can change any order, Agent can change their assigned orders
        if not current_user.is_admin:
            if current_user.is_agent and order.agent_id != current_user.id:
                return jsonify(build_error_response('PERMISSION_DENIED', 'You can only change status of orders assigned to you')[0]), 403
            elif current_user.is_client:
                return jsonify(build_error_response('PERMISSION_DENIED', 'Clients cannot change order status')[0]), 403
        
        success, error = OrderService.change_order_status(order_id, new_status, current_user.id)
        
        if not success:
            return jsonify(build_error_response('VALIDATION_ERROR', error)[0]), 400
        
        # Return updated order data
        updated_order = Order.get_by_id(order_id)
        return jsonify(build_success_response(updated_order.to_dict(include_relations=True), 'Order status updated')[0]), 200
    
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f'Error changing order status {order_id}: {str(e)}', exc_info=True)
        return jsonify(build_error_response('SERVER_ERROR', f'Failed to change status: {str(e)}')[0]), 500


@orders_bp.route('/<int:order_id>/assign', methods=['PATCH'])
@login_required
@admin_required
def assign_order(order_id):
    """PATCH /api/orders/:id/assign - Assign order to agent."""
    from flask import current_app
    
    try:
        data = request.get_json()
        
        if data is None:
            return jsonify(build_error_response('VALIDATION_ERROR', 'Request body required')[0]), 400
        
        # Get order
        order = Order.get_by_id(order_id)
        if not order:
            return jsonify(build_error_response('NOT_FOUND', 'Order not found')[0]), 404
        
        agent_id = data.get('agent_id')
        
        # If agent_id is None or empty string, unassign
        if agent_id is None or agent_id == '':
            old_agent_id = order.agent_id
            order.agent_id = None
            order.save()
            
            # Log the action
            from app.models.audit_log import AuditLog
            AuditLog.log_action(
                action='ORDER_UNASSIGNED',
                user_id=current_user.id,
                details={
                    'order_id': order_id,
                    'previous_agent_id': old_agent_id
                }
            )
            
            # Notify previous agent
            if old_agent_id:
                from app.services.notification_service import NotificationService
                NotificationService.create_notification(
                    user_id=old_agent_id,
                    message=f'Order #{order_id} has been unassigned from you.',
                    related_order_id=order_id
                )
            
            return jsonify(build_success_response(order.to_dict(include_relations=True), 'Order unassigned')[0]), 200
        
        # Convert to int if string
        try:
            agent_id = int(agent_id)
        except (ValueError, TypeError):
            return jsonify(build_error_response('VALIDATION_ERROR', 'Invalid agent ID format')[0]), 400
        
        # Validate agent
        agent = User.get_by_id(agent_id)
        if not agent or not agent.is_agent:
            return jsonify(build_error_response('VALIDATION_ERROR', 'Invalid agent ID')[0]), 400
        
        if not agent.is_active:
            return jsonify(build_error_response('VALIDATION_ERROR', 'Agent account is not active')[0]), 400
        
        # Check agent workload limit (only for new assignments, not reassignments)
        if order.agent_id != agent_id:
            max_limit = current_app.config.get('MAX_ACTIVE_ORDERS_DEFAULT', 10)
            active_count = agent.get_active_orders_count()
            
            # If assigning to new agent and they're at limit
            if order.agent_id is None and not agent.can_accept_order(max_limit):
                return jsonify(build_error_response(
                    'AGENT_LIMIT_EXCEEDED',
                    f'Agent workload limit exceeded. Active orders: {active_count}/{max_limit}'
                )[0]), 400
        
        # Assign order
        old_agent_id = order.agent_id
        order.agent_id = agent_id
        order.save()
        
        # Log the action
        from app.models.audit_log import AuditLog
        AuditLog.log_action(
            action='ORDER_ASSIGNED' if old_agent_id is None else 'ORDER_REASSIGNED',
            user_id=current_user.id,
            details={
                'order_id': order_id,
                'agent_id': agent_id,
                'previous_agent_id': old_agent_id
            }
        )
        
        # Send notifications
        from app.services.notification_service import NotificationService
        
        # Notify new agent
        NotificationService.create_notification(
            user_id=agent_id,
            message=f'Order #{order_id} has been assigned to you by {current_user.email}.',
            related_order_id=order_id,
            send_email=True
        )
        
        # Notify previous agent if reassignment
        if old_agent_id and old_agent_id != agent_id:
            NotificationService.create_notification(
                user_id=old_agent_id,
                message=f'Order #{order_id} has been reassigned to another agent.',
                related_order_id=order_id
            )
        
        return jsonify(build_success_response(order.to_dict(include_relations=True), 'Order assigned successfully')[0]), 200
    
    except Exception as e:
        current_app.logger.error(f'Error assigning order {order_id}: {str(e)}', exc_info=True)
        return jsonify(build_error_response('SERVER_ERROR', f'Failed to assign order: {str(e)}')[0]), 500
