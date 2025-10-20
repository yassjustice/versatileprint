"""
Authentication service.
Handles user login, logout, and session management.
"""
from typing import Optional, Tuple
from flask_login import login_user, logout_user
from app.models.user import User
from app.models.audit_log import AuditLog


class AuthService:
    """Authentication service."""
    
    @staticmethod
    def authenticate(email: str, password: str, remember: bool = False, ip_address: str = None, user_agent: str = None) -> Tuple[bool, Optional[User], Optional[str]]:
        """
        Authenticate user with email and password.
        
        Args:
            email: User email
            password: User password
            remember: Remember user session
            ip_address: Client IP address for audit
            user_agent: User agent for audit
        
        Returns:
            (success, user, error_message)
        """
        # Find user by email
        user = User.get_by_email(email)
        
        if not user:
            # Log failed attempt
            AuditLog.log_action(
                action='USER_LOGIN_FAILED',
                user_id=None,
                details={'email': email, 'reason': 'user_not_found'},
                ip_address=ip_address,
                user_agent=user_agent
            )
            return False, None, 'Invalid email or password'
        
        # Check if account is active
        if not user.is_active:
            # Log failed attempt
            AuditLog.log_action(
                action='USER_LOGIN_FAILED',
                user_id=user.id,
                details={'email': email, 'reason': 'account_disabled'},
                ip_address=ip_address,
                user_agent=user_agent
            )
            return False, None, 'Account is disabled. Please contact administrator.'
        
        # Verify password
        if not user.check_password(password):
            # Log failed attempt
            AuditLog.log_action(
                action='USER_LOGIN_FAILED',
                user_id=user.id,
                details={'email': email, 'reason': 'invalid_password'},
                ip_address=ip_address,
                user_agent=user_agent
            )
            return False, None, 'Invalid email or password'
        
        # Login successful - update last login
        user.update_last_login()
        
        # Log in user
        login_user(user, remember=remember)
        
        # Log successful login
        AuditLog.log_action(
            action='USER_LOGIN_SUCCESS',
            user_id=user.id,
            details={'email': email},
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return True, user, None
    
    @staticmethod
    def logout(user_id: int, ip_address: str = None, user_agent: str = None):
        """
        Logout current user.
        
        Args:
            user_id: User ID for audit
            ip_address: Client IP address for audit
            user_agent: User agent for audit
        """
        # Log logout
        AuditLog.log_action(
            action='USER_LOGOUT',
            user_id=user_id,
            details={},
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Logout user
        logout_user()
    
    @staticmethod
    def change_password(user: User, old_password: str, new_password: str) -> Tuple[bool, Optional[str]]:
        """
        Change user password.
        
        Args:
            user: User object
            old_password: Current password
            new_password: New password
        
        Returns:
            (success, error_message)
        """
        from app.utils.validators import validate_password
        
        # Verify old password
        if not user.check_password(old_password):
            return False, 'Current password is incorrect'
        
        # Validate new password
        valid, error = validate_password(new_password)
        if not valid:
            return False, error
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        # Log password change
        AuditLog.log_action(
            action='PASSWORD_CHANGED',
            user_id=user.id,
            details={'email': user.email}
        )
        
        return True, None
    
    @staticmethod
    def reset_password(user: User, new_password: str, admin_id: int) -> Tuple[bool, Optional[str]]:
        """
        Reset user password (admin action).
        
        Args:
            user: User object
            new_password: New password
            admin_id: Administrator performing reset
        
        Returns:
            (success, error_message)
        """
        from app.utils.validators import validate_password
        
        # Validate new password
        valid, error = validate_password(new_password)
        if not valid:
            return False, error
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        # Log password reset
        AuditLog.log_action(
            action='PASSWORD_RESET',
            user_id=admin_id,
            details={
                'target_user_id': user.id,
                'target_email': user.email
            }
        )
        
        return True, None
