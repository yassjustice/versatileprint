"""
Authentication API endpoints.
Handles login, logout, and password operations.
"""
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from app.services.auth_service import AuthService
from app.utils.decorators import rate_limit
from app.utils.helpers import get_client_ip, get_user_agent, build_error_response, build_success_response

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
@rate_limit(max_requests=5, window_seconds=300)  # 5 attempts per 5 minutes
def login():
    """
    User login endpoint.
    
    POST /api/auth/login
    Body: {email, password, remember}
    """
    data = request.get_json()
    
    if not data:
        return jsonify(build_error_response('VALIDATION_ERROR', 'Request body is required')[0]), 400
    
    email = data.get('email', '').strip()
    password = data.get('password', '')
    remember = data.get('remember', False)
    
    if not email or not password:
        return jsonify(build_error_response('VALIDATION_ERROR', 'Email and password are required')[0]), 400
    
    # Authenticate
    success, user, error = AuthService.authenticate(
        email=email,
        password=password,
        remember=remember,
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )
    
    if not success:
        return jsonify(build_error_response('AUTH_FAILED', error or 'Authentication failed')[0]), 401
    
    # Return user data
    response_data = {
        'user': user.to_dict(include_role=True),
        'message': 'Login successful'
    }
    
    return jsonify(build_success_response(response_data, status_code=200)[0]), 200


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    User logout endpoint.
    
    POST /api/auth/logout
    """
    user_id = current_user.id
    
    AuthService.logout(
        user_id=user_id,
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )
    
    return '', 204


@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """
    Get current authenticated user.
    
    GET /api/auth/me
    """
    return jsonify(build_success_response(current_user.to_dict(include_role=True))[0]), 200


@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """
    Change password for current user.
    
    POST /api/auth/change-password
    Body: {old_password, new_password}
    """
    data = request.get_json()
    
    if not data:
        return jsonify(build_error_response('VALIDATION_ERROR', 'Request body is required')[0]), 400
    
    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')
    
    if not old_password or not new_password:
        return jsonify(build_error_response('VALIDATION_ERROR', 'Both old_password and new_password are required')[0]), 400
    
    success, error = AuthService.change_password(current_user, old_password, new_password)
    
    if not success:
        return jsonify(build_error_response('VALIDATION_ERROR', error)[0]), 400
    
    return jsonify(build_success_response(message='Password changed successfully')[0]), 200
