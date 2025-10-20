"""
Helper utilities and common functions.
"""
from datetime import datetime, date
from typing import Dict, Any, Optional
import secrets
import string
import os


def generate_secure_filename(original_filename: str, prefix: str = '') -> str:
    """
    Generate a secure unique filename.
    
    Args:
        original_filename: Original filename with extension
        prefix: Optional prefix for the filename
    
    Returns:
        Secure filename with timestamp and random string
    """
    from app.utils.validators import sanitize_filename
    
    # Sanitize original filename
    safe_filename = sanitize_filename(original_filename)
    
    # Split name and extension
    name_parts = safe_filename.rsplit('.', 1)
    name = name_parts[0] if len(name_parts) > 0 else 'file'
    ext = name_parts[1] if len(name_parts) > 1 else ''
    
    # Generate timestamp
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    
    # Generate random string
    random_str = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    
    # Build filename
    parts = [part for part in [prefix, timestamp, random_str, name] if part]
    filename = '_'.join(parts)
    
    if ext:
        filename = f'{filename}.{ext}'
    
    return filename


def normalize_month(dt: date) -> date:
    """Normalize date to first day of month."""
    return dt.replace(day=1)


def get_current_month() -> date:
    """Get current month normalized to first day."""
    return normalize_month(datetime.utcnow().date())


def format_datetime(dt: Optional[datetime], format_str: str = '%Y-%m-%d %H:%M:%S') -> Optional[str]:
    """Format datetime to string."""
    if not dt:
        return None
    return dt.strftime(format_str)


def format_date(d: Optional[date], format_str: str = '%Y-%m-%d') -> Optional[str]:
    """Format date to string."""
    if not d:
        return None
    return d.strftime(format_str)


def parse_date(date_str: str, format_str: str = '%Y-%m-%d') -> Optional[date]:
    """Parse date string to date object."""
    try:
        return datetime.strptime(date_str, format_str).date()
    except (ValueError, TypeError):
        return None


def build_error_response(code: str, message: str, details: Any = None, status_code: int = 400) -> tuple:
    """
    Build standardized JSON error response.
    
    Args:
        code: Error code (e.g., 'VALIDATION_ERROR')
        message: Human-readable error message
        details: Additional error details
        status_code: HTTP status code
    
    Returns:
        (response_dict, status_code)
    """
    response = {
        'error': {
            'code': code,
            'message': message
        }
    }
    
    if details is not None:
        response['error']['details'] = details
    
    return response, status_code


def build_success_response(data: Any = None, message: str = None, status_code: int = 200) -> tuple:
    """
    Build standardized JSON success response.
    
    Args:
        data: Response data
        message: Optional success message
        status_code: HTTP status code
    
    Returns:
        (response_dict, status_code)
    """
    response = {}
    
    if message:
        response['message'] = message
    
    if data is not None:
        response['data'] = data
    
    return response, status_code


def paginate_query_results(items: list, page: int = 1, page_size: int = 20, default_page_size: int = 20, max_page_size: int = 100) -> dict:
    """
    Paginate query results.
    
    Args:
        items: List of items to paginate
        page: Page number (1-indexed)
        page_size: Items per page
        default_page_size: Default page size
        max_page_size: Maximum allowed page size
    
    Returns:
        Paginated response dictionary
    """
    # Validate and normalize pagination params
    page = max(1, page)
    page_size = min(max(1, page_size or default_page_size), max_page_size)
    
    # Calculate pagination
    total_items = len(items)
    total_pages = (total_items + page_size - 1) // page_size
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    
    # Get page items
    page_items = items[start_index:end_index]
    
    return {
        'items': page_items,
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total_items': total_items,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }


def allowed_file(filename: str, allowed_extensions: set = None) -> bool:
    """
    Check if filename has an allowed extension.
    
    Args:
        filename: Filename to check
        allowed_extensions: Set of allowed extensions (default: {'csv'})
    
    Returns:
        True if allowed, False otherwise
    """
    if allowed_extensions is None:
        allowed_extensions = {'csv'}
    
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def get_client_ip(request) -> str:
    """Extract client IP address from request."""
    # Check for proxy headers
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr or 'unknown'


def get_user_agent(request) -> str:
    """Extract user agent from request."""
    return request.headers.get('User-Agent', 'unknown')


def calculate_percentage(part: int, total: int, decimals: int = 2) -> float:
    """
    Calculate percentage safely.
    
    Args:
        part: Part value
        total: Total value
        decimals: Number of decimal places
    
    Returns:
        Percentage as float
    """
    if total == 0:
        return 0.0
    return round((part / total) * 100, decimals)


def ensure_directory_exists(directory_path: str):
    """Create directory if it doesn't exist."""
    os.makedirs(directory_path, exist_ok=True)


def format_quota_message(quota_type: str, available: int, total: int, requested: int) -> str:
    """
    Format a user-friendly quota error message.
    
    Args:
        quota_type: 'B&W' or 'Color'
        available: Available quota
        total: Total quota (including top-ups)
        requested: Requested amount
    
    Returns:
        Formatted message
    """
    used = total - available
    percentage = calculate_percentage(used, total)
    
    return (
        f'Insufficient {quota_type} quota. '
        f'Available: {available}/{total} ({percentage:.1f}% used). '
        f'Requested: {requested}. '
        f'Please reduce quantity or request a top-up.'
    )
