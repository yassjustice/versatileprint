"""
User management API endpoints (Admin only).
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app.models.user import User, Role
from app.utils.decorators import admin_required
from app.utils.helpers import build_error_response, build_success_response, paginate_query_results
from app.utils.validators import validate_email, validate_password

users_bp = Blueprint('users', __name__)


@users_bp.route('', methods=['GET'])
@login_required
@admin_required
def list_users():
    """GET /api/users - List all users with optional filters."""
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    role = request.args.get('role')
    is_active = request.args.get('is_active')
    
    users = User.get_all()
    
    if role:
        users = [u for u in users if u.role_name == role]
    
    if is_active is not None:
        active_filter = is_active.lower() == 'true'
        users = [u for u in users if u.is_active == active_filter]
    
    # Include active_orders_count for agents
    users_data = []
    for u in users:
        user_dict = u.to_dict(include_role=True)
        if u.is_agent:
            user_dict['active_orders_count'] = u.get_active_orders_count()
            user_dict['max_capacity'] = 10  # Could come from config
        users_data.append(user_dict)
    
    result = paginate_query_results(users_data, page, page_size)
    
    return jsonify(build_success_response(result)[0]), 200


@users_bp.route('', methods=['POST'])
@login_required
@admin_required
def create_user():
    """POST /api/users - Create new user."""
    from flask import current_app
    
    data = request.get_json()
    
    # Log the incoming request for debugging
    current_app.logger.info(f'POST /api/users - Request data: {data}')
    
    if not data:
        error_msg = 'Request body required'
        current_app.logger.warning(f'User creation failed: {error_msg}')
        return jsonify(build_error_response('VALIDATION_ERROR', error_msg)[0]), 400
    
    email = data.get('email', '').strip() if data.get('email') else ''
    password = data.get('password', '') if data.get('password') else ''
    full_name = data.get('full_name', '').strip() if data.get('full_name') else ''
    role_name = data.get('role', '').strip() if data.get('role') else ''
    
    # Validate required fields
    if not email:
        error_msg = 'Email is required'
        current_app.logger.warning(f'User creation failed: {error_msg}')
        return jsonify(build_error_response('VALIDATION_ERROR', error_msg)[0]), 400
    
    if not password:
        error_msg = 'Password is required'
        current_app.logger.warning(f'User creation failed: {error_msg}')
        return jsonify(build_error_response('VALIDATION_ERROR', error_msg)[0]), 400
    
    if not role_name:
        error_msg = 'Role is required'
        current_app.logger.warning(f'User creation failed: {error_msg}')
        return jsonify(build_error_response('VALIDATION_ERROR', error_msg)[0]), 400
    
    # Validate email
    valid, error = validate_email(email)
    if not valid:
        current_app.logger.warning(f'User creation failed - Email validation: {error}')
        return jsonify(build_error_response('VALIDATION_ERROR', error)[0]), 400
    
    # Validate password
    valid, error = validate_password(password)
    if not valid:
        current_app.logger.warning(f'User creation failed - Password validation: {error}')
        return jsonify(build_error_response('VALIDATION_ERROR', error)[0]), 400
    
    if role_name not in ['Client', 'Agent', 'Administrator']:
        error_msg = f'Invalid role "{role_name}". Must be Client, Agent, or Administrator'
        current_app.logger.warning(f'User creation failed: {error_msg}')
        return jsonify(build_error_response('VALIDATION_ERROR', error_msg)[0]), 400
    
    try:
        user = User.create_user(email, password, full_name, role_name)
        current_app.logger.info(f'User created successfully: {email} (ID: {user.id})')
        return jsonify(build_success_response(user.to_dict(include_role=True), 'User created successfully', 201)[0]), 201
    except ValueError as e:
        error_msg = str(e)
        current_app.logger.error(f'User creation failed - ValueError: {error_msg}')
        return jsonify(build_error_response('VALIDATION_ERROR', error_msg)[0]), 400
    except Exception as e:
        error_msg = f'Unexpected error: {str(e)}'
        current_app.logger.error(f'User creation failed - Exception: {error_msg}', exc_info=True)
        return jsonify(build_error_response('SERVER_ERROR', 'An unexpected error occurred')[0]), 500


@users_bp.route('/<int:user_id>', methods=['GET'])
@login_required
@admin_required
def get_user(user_id):
    """GET /api/users/:id - Get user details."""
    user = User.get_by_id(user_id)
    if not user:
        return jsonify(build_error_response('NOT_FOUND', 'User not found')[0]), 404
    
    return jsonify(build_success_response(user.to_dict(include_role=True))[0]), 200


@users_bp.route('/<int:user_id>', methods=['PATCH', 'PUT'])
@login_required
@admin_required
def update_user(user_id):
    """PATCH/PUT /api/users/:id - Update user."""
    from flask import current_app
    
    try:
        user = User.get_by_id(user_id)
        if not user:
            return jsonify(build_error_response('NOT_FOUND', 'User not found')[0]), 404
        
        data = request.get_json()
        if not data:
            return jsonify(build_error_response('VALIDATION_ERROR', 'Request body required')[0]), 400
        
        current_app.logger.info(f'Updating user {user_id} with data: {data}')
        
        # Track if any changes were made
        changes_made = False
        
        if 'full_name' in data:
            user.full_name = data['full_name']
            changes_made = True
            current_app.logger.info(f'Updated full_name to: {data["full_name"]}')
        
        if 'is_active' in data:
            user.is_active = bool(data['is_active'])
            changes_made = True
            current_app.logger.info(f'Updated is_active to: {data["is_active"]}')
        
        if 'role' in data:
            role = Role.get_by_name(data['role'])
            if role:
                user.role_id = role.id
                changes_made = True
                current_app.logger.info(f'Updated role to: {data["role"]}')
            else:
                return jsonify(build_error_response('VALIDATION_ERROR', f'Invalid role: {data["role"]}')[0]), 400
        
        if not changes_made:
            return jsonify(build_success_response(user.to_dict(include_role=True), 'No changes made')[0]), 200
        
        user.save()
        current_app.logger.info(f'User {user_id} updated successfully')
        
        return jsonify(build_success_response(user.to_dict(include_role=True), 'User updated successfully')[0]), 200
    
    except Exception as e:
        current_app.logger.error(f'Error updating user {user_id}: {str(e)}', exc_info=True)
        return jsonify(build_error_response('SERVER_ERROR', f'Failed to update user: {str(e)}')[0]), 500


@users_bp.route('/<int:user_id>/reset-password', methods=['POST'])
@login_required
@admin_required
def reset_password(user_id):
    """POST /api/users/:id/reset-password - Reset user password."""
    user = User.get_by_id(user_id)
    if not user:
        return jsonify(build_error_response('NOT_FOUND', 'User not found')[0]), 404
    
    data = request.get_json()
    new_password = data.get('new_password', '')
    
    valid, error = validate_password(new_password)
    if not valid:
        return jsonify(build_error_response('VALIDATION_ERROR', error)[0]), 400
    
    from app.services.auth_service import AuthService
    success, error = AuthService.reset_password(user, new_password, current_user.id)
    
    if not success:
        return jsonify(build_error_response('VALIDATION_ERROR', error)[0]), 400
    
    return jsonify(build_success_response(message='Password reset successfully')[0]), 200


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    """DELETE /api/users/:id - Delete user (soft delete by deactivating)."""
    from flask import current_app
    
    # Prevent self-deletion
    if user_id == current_user.id:
        return jsonify(build_error_response('VALIDATION_ERROR', 'Cannot delete your own account')[0]), 400
    
    user = User.get_by_id(user_id)
    if not user:
        return jsonify(build_error_response('NOT_FOUND', 'User not found')[0]), 404
    
    # Check if user has active orders
    if user.is_client:
        from app.models.order import Order, OrderStatus
        session = user.get_session()
        active_orders = session.query(Order).filter(
            Order.client_id == user_id,
            Order.status.in_([OrderStatus.PENDING, OrderStatus.VALIDATED, OrderStatus.PROCESSING])
        ).count()
        
        if active_orders > 0:
            return jsonify(build_error_response(
                'VALIDATION_ERROR', 
                f'Cannot delete user with {active_orders} active order(s). Complete or cancel them first.'
            )[0]), 400
    
    elif user.is_agent:
        from app.models.order import Order, OrderStatus
        session = user.get_session()
        active_orders = session.query(Order).filter(
            Order.agent_id == user_id,
            Order.status.in_([OrderStatus.PENDING, OrderStatus.VALIDATED, OrderStatus.PROCESSING])
        ).count()
        
        if active_orders > 0:
            return jsonify(build_error_response(
                'VALIDATION_ERROR', 
                f'Cannot delete agent with {active_orders} active order(s). Reassign them first.'
            )[0]), 400
    
    # Perform soft delete (deactivate)
    user.is_active = False
    user.save()
    
    # Log the action
    from app.models.audit_log import AuditLog
    AuditLog.log_action(
        action='USER_DELETED',
        user_id=current_user.id,
        details={
            'deleted_user_id': user_id,
            'deleted_user_email': user.email,
            'deleted_user_role': user.role_name
        }
    )
    
    current_app.logger.info(f'User {user.email} (ID: {user_id}) deactivated by {current_user.email}')
    
    return jsonify(build_success_response(message='User deleted successfully')[0]), 200
