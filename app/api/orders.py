"""
Order management API endpoints.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

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
@admin_required
def change_status(order_id):
    """POST /api/orders/:id/status - Change order status."""
    data = request.get_json()
    
    if not data or not data.get('status'):
        return jsonify(build_error_response('VALIDATION_ERROR', 'Status is required')[0]), 400
    
    new_status = data['status']
    
    success, error = OrderService.change_order_status(order_id, new_status, current_user.id)
    
    if not success:
        return jsonify(build_error_response('VALIDATION_ERROR', error)[0]), 400
    
    return jsonify(build_success_response(message='Order status updated')[0]), 200
