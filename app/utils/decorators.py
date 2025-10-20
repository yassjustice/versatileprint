"""
Authentication and authorization decorators.
RBAC enforcement for routes and functions.
"""
from functools import wraps
from flask import jsonify, abort, request
from flask_login import current_user


def login_required_api(f):
    """Decorator for API endpoints requiring authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({
                'error': {
                    'code': 'AUTH_FAILED',
                    'message': 'Authentication required',
                    'details': 'Please log in to access this endpoint'
                }
            }), 401
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    """
    Decorator to require specific role(s) for access.
    Usage: @role_required('Administrator', 'Agent')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                if request.path.startswith('/api/'):
                    return jsonify({
                        'error': {
                            'code': 'AUTH_FAILED',
                            'message': 'Authentication required',
                            'details': 'Please log in to access this endpoint'
                        }
                    }), 401
                abort(401)
            
            if current_user.role_name not in roles:
                if request.path.startswith('/api/'):
                    return jsonify({
                        'error': {
                            'code': 'PERMISSION_DENIED',
                            'message': 'Access forbidden',
                            'details': f'This endpoint requires one of these roles: {", ".join(roles)}'
                        }
                    }), 403
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """Decorator to require Administrator role."""
    return role_required('Administrator')(f)


def agent_or_admin_required(f):
    """Decorator to require Agent or Administrator role."""
    return role_required('Agent', 'Administrator')(f)


def client_required(f):
    """Decorator to require Client role."""
    return role_required('Client')(f)


def check_active_user(f):
    """Decorator to ensure user account is active."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            if request.path.startswith('/api/'):
                return jsonify({
                    'error': {
                        'code': 'AUTH_FAILED',
                        'message': 'Authentication required'
                    }
                }), 401
            abort(401)
        
        if not current_user.is_active:
            if request.path.startswith('/api/'):
                return jsonify({
                    'error': {
                        'code': 'ACCOUNT_DISABLED',
                        'message': 'Account is disabled',
                        'details': 'Your account has been deactivated. Please contact administrator.'
                    }
                }), 403
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def owns_resource_or_admin(resource_owner_id_param='id'):
    """
    Decorator to check if user owns the resource or is admin.
    
    Args:
        resource_owner_id_param: Name of the parameter containing the owner's user_id
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                if request.path.startswith('/api/'):
                    return jsonify({
                        'error': {
                            'code': 'AUTH_FAILED',
                            'message': 'Authentication required'
                        }
                    }), 401
                abort(401)
            
            # Admins can access anything
            if current_user.is_admin:
                return f(*args, **kwargs)
            
            # Check resource ownership
            owner_id = kwargs.get(resource_owner_id_param) or request.view_args.get(resource_owner_id_param)
            
            if owner_id and int(owner_id) != current_user.id:
                if request.path.startswith('/api/'):
                    return jsonify({
                        'error': {
                            'code': 'PERMISSION_DENIED',
                            'message': 'Access forbidden',
                            'details': 'You can only access your own resources'
                        }
                    }), 403
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def rate_limit(max_requests=5, window_seconds=60):
    """
    Simple rate limiting decorator.
    
    Args:
        max_requests: Maximum requests allowed in window
        window_seconds: Time window in seconds
    
    Note: This is a basic implementation. For production, use Flask-Limiter or similar.
    """
    from collections import defaultdict
    from time import time
    
    # Store request timestamps per IP
    request_history = defaultdict(list)
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client IP
            client_ip = request.remote_addr
            
            # Get current timestamp
            now = time()
            
            # Clean old entries
            request_history[client_ip] = [
                ts for ts in request_history[client_ip]
                if now - ts < window_seconds
            ]
            
            # Check rate limit
            if len(request_history[client_ip]) >= max_requests:
                if request.path.startswith('/api/'):
                    return jsonify({
                        'error': {
                            'code': 'RATE_LIMIT_EXCEEDED',
                            'message': 'Too many requests',
                            'details': f'Maximum {max_requests} requests per {window_seconds} seconds'
                        }
                    }), 429
                abort(429)
            
            # Record this request
            request_history[client_ip].append(now)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
