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
    
    users_data = [u.to_dict(include_role=True) for u in users]
    result = paginate_query_results(users_data, page, page_size)
    
    return jsonify(build_success_response(result)[0]), 200


@users_bp.route('', methods=['POST'])
@login_required
@admin_required
def create_user():
    """POST /api/users - Create new user."""
    data = request.get_json()
    
    if not data:
        return jsonify(build_error_response('VALIDATION_ERROR', 'Request body required')[0]), 400
    
    email = data.get('email', '').strip()
    password = data.get('password', '')
    full_name = data.get('full_name', '').strip()
    role_name = data.get('role', '').strip()
    
    # Validate required fields
    if not email:
        return jsonify(build_error_response('VALIDATION_ERROR', 'Email is required')[0]), 400
    
    if not password:
        return jsonify(build_error_response('VALIDATION_ERROR', 'Password is required')[0]), 400
    
    if not role_name:
        return jsonify(build_error_response('VALIDATION_ERROR', 'Role is required')[0]), 400
    
    # Validate email
    valid, error = validate_email(email)
    if not valid:
        return jsonify(build_error_response('VALIDATION_ERROR', error)[0]), 400
    
    # Validate password
    valid, error = validate_password(password)
    if not valid:
        return jsonify(build_error_response('VALIDATION_ERROR', error)[0]), 400
    
    if role_name not in ['Client', 'Agent', 'Administrator']:
        return jsonify(build_error_response('VALIDATION_ERROR', 'Invalid role. Must be Client, Agent, or Administrator')[0]), 400
    
    try:
        user = User.create_user(email, password, full_name, role_name)
        return jsonify(build_success_response(user.to_dict(include_role=True), 'User created successfully', 201)[0]), 201
    except ValueError as e:
        return jsonify(build_error_response('VALIDATION_ERROR', str(e))[0]), 400


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
    user = User.get_by_id(user_id)
    if not user:
        return jsonify(build_error_response('NOT_FOUND', 'User not found')[0]), 404
    
    data = request.get_json()
    if not data:
        return jsonify(build_error_response('VALIDATION_ERROR', 'Request body required')[0]), 400
    
    if 'full_name' in data:
        user.full_name = data['full_name']
    
    if 'is_active' in data:
        user.is_active = bool(data['is_active'])
    
    if 'role' in data:
        role = Role.get_by_name(data['role'])
        if role:
            user.role_id = role.id
    
    user.save()
    
    return jsonify(build_success_response(user.to_dict(include_role=True), 'User updated')[0]), 200


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
