"""
Validation utilities for user inputs.
"""
import re
from typing import Tuple, Optional
import phonenumbers
from email_validator import validate_email as validate_email_lib, EmailNotValidError


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email address format.
    
    Returns:
        (is_valid, error_message)
    """
    try:
        validated = validate_email_lib(email, check_deliverability=False)
        return True, None
    except EmailNotValidError as e:
        return False, str(e)


def validate_phone(phone: str, pattern: str = r'^\+?[1-9]\d{1,14}$') -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Validate and normalize phone number.
    
    Args:
        phone: Phone number to validate
        pattern: Regex pattern for validation
    
    Returns:
        (is_valid, normalized_phone, error_message)
    """
    if not phone:
        return True, None, None  # Phone is optional
    
    # Remove whitespace
    phone = phone.strip()
    
    try:
        # Try to parse with phonenumbers library
        parsed = phonenumbers.parse(phone, None)
        if phonenumbers.is_valid_number(parsed):
            normalized = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            return True, normalized, None
    except:
        pass
    
    # Fallback to regex pattern
    if re.match(pattern, phone):
        return True, phone, None
    
    return False, None, f'Invalid phone number format. Expected pattern: {pattern}'


def validate_password(password: str, min_length: int = 8) -> Tuple[bool, Optional[str]]:
    """
    Validate password strength.
    
    Requirements:
    - Minimum length
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    
    Returns:
        (is_valid, error_message)
    """
    if len(password) < min_length:
        return False, f'Password must be at least {min_length} characters long'
    
    if not re.search(r'[A-Z]', password):
        return False, 'Password must contain at least one uppercase letter'
    
    if not re.search(r'[a-z]', password):
        return False, 'Password must contain at least one lowercase letter'
    
    if not re.search(r'\d', password):
        return False, 'Password must contain at least one digit'
    
    return True, None


def validate_paper_dimensions(dimensions: str) -> Tuple[bool, Optional[str]]:
    """
    Validate paper dimensions format.
    
    Accepts: A4, A3, A5, or custom format like 210x297mm
    
    Returns:
        (is_valid, error_message)
    """
    if not dimensions:
        return True, None  # Optional field
    
    dimensions = dimensions.strip().upper()
    
    # Standard sizes
    standard_sizes = ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'LETTER', 'LEGAL', 'TABLOID']
    if dimensions in standard_sizes:
        return True, None
    
    # Custom format: WIDTHxHEIGHTmm or WIDTHxHEIGHTcm
    if re.match(r'^\d+x\d+(mm|cm)$', dimensions.lower()):
        return True, None
    
    return False, f'Invalid paper dimensions. Use standard sizes ({", ".join(standard_sizes[:5])}, etc.) or format like "210x297mm"'


def validate_integer(value: any, min_value: int = 0, max_value: int = None, field_name: str = 'value') -> Tuple[bool, Optional[int], Optional[str]]:
    """
    Validate and convert integer value.
    
    Returns:
        (is_valid, converted_value, error_message)
    """
    try:
        int_value = int(value)
        
        if int_value < min_value:
            return False, None, f'{field_name} must be at least {min_value}'
        
        if max_value is not None and int_value > max_value:
            return False, None, f'{field_name} must not exceed {max_value}'
        
        return True, int_value, None
    
    except (ValueError, TypeError):
        return False, None, f'{field_name} must be a valid integer'


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """
    Sanitize filename for safe storage.
    
    Removes path traversal attempts and dangerous characters.
    """
    if not filename:
        return 'unnamed'
    
    # Remove path separators
    filename = filename.replace('/', '_').replace('\\', '_')
    
    # Remove dangerous characters
    filename = re.sub(r'[^\w\s\-\.]', '_', filename)
    
    # Limit length
    if len(filename) > max_length:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        max_name_length = max_length - len(ext) - 1
        filename = name[:max_name_length] + ('.' + ext if ext else '')
    
    return filename


def validate_csv_row_data(row_data: dict, row_number: int) -> Tuple[bool, list]:
    """
    Validate a single CSV row.
    
    Returns:
        (is_valid, list_of_errors)
    """
    errors = []
    
    # Check required fields
    if not row_data.get('client_id') and not row_data.get('client_email'):
        errors.append(f'Row {row_number}: Either client_id or client_email is required')
    
    # Validate quantities
    bw_valid, bw_value, bw_error = validate_integer(
        row_data.get('bw_quantity', 0),
        min_value=0,
        field_name='bw_quantity'
    )
    if not bw_valid:
        errors.append(f'Row {row_number}: {bw_error}')
    
    color_valid, color_value, color_error = validate_integer(
        row_data.get('color_quantity', 0),
        min_value=0,
        field_name='color_quantity'
    )
    if not color_valid:
        errors.append(f'Row {row_number}: {color_error}')
    
    # At least one quantity must be > 0
    if bw_valid and color_valid and (bw_value or 0) == 0 and (color_value or 0) == 0:
        errors.append(f'Row {row_number}: At least one of bw_quantity or color_quantity must be greater than 0')
    
    # Validate email if provided
    if row_data.get('client_email'):
        email_valid, email_error = validate_email(row_data['client_email'])
        if not email_valid:
            errors.append(f'Row {row_number}: {email_error}')
    
    if row_data.get('agent_email'):
        email_valid, email_error = validate_email(row_data['agent_email'])
        if not email_valid:
            errors.append(f'Row {row_number}: Agent email - {email_error}')
    
    # Validate phone if provided
    if row_data.get('client_phone'):
        phone_valid, normalized, phone_error = validate_phone(row_data['client_phone'])
        if not phone_valid:
            errors.append(f'Row {row_number}: {phone_error}')
    
    # Validate paper dimensions if provided
    if row_data.get('paper_dimensions'):
        dim_valid, dim_error = validate_paper_dimensions(row_data['paper_dimensions'])
        if not dim_valid:
            errors.append(f'Row {row_number}: {dim_error}')
    
    return len(errors) == 0, errors


def validate_order_data(data: dict) -> Tuple[bool, dict, list]:
    """
    Validate order creation data.
    
    Returns:
        (is_valid, validated_data, errors)
    """
    errors = []
    validated = {}
    
    # Validate client_id (required)
    if not data.get('client_id'):
        errors.append('client_id is required')
    else:
        valid, value, error = validate_integer(data['client_id'], min_value=1, field_name='client_id')
        if valid:
            validated['client_id'] = value
        else:
            errors.append(error)
    
    # Validate agent_id (optional)
    if data.get('agent_id'):
        valid, value, error = validate_integer(data['agent_id'], min_value=1, field_name='agent_id')
        if valid:
            validated['agent_id'] = value
        else:
            errors.append(error)
    
    # Validate quantities
    bw_valid, bw_value, bw_error = validate_integer(
        data.get('bw_quantity', 0),
        min_value=0,
        field_name='bw_quantity'
    )
    if bw_valid:
        validated['bw_quantity'] = bw_value
    else:
        errors.append(bw_error)
    
    color_valid, color_value, color_error = validate_integer(
        data.get('color_quantity', 0),
        min_value=0,
        field_name='color_quantity'
    )
    if color_valid:
        validated['color_quantity'] = color_value
    else:
        errors.append(color_error)
    
    # At least one quantity must be > 0
    if bw_valid and color_valid and validated.get('bw_quantity', 0) == 0 and validated.get('color_quantity', 0) == 0:
        errors.append('At least one of bw_quantity or color_quantity must be greater than 0')
    
    # Validate paper dimensions (optional)
    if data.get('paper_dimensions'):
        dim_valid, dim_error = validate_paper_dimensions(data['paper_dimensions'])
        if dim_valid:
            validated['paper_dimensions'] = data['paper_dimensions']
        else:
            errors.append(dim_error)
    
    # Optional string fields
    if data.get('paper_type'):
        validated['paper_type'] = str(data['paper_type'])[:100]
    
    if data.get('finishing'):
        validated['finishing'] = str(data['finishing'])[:100]
    
    if data.get('notes'):
        validated['notes'] = str(data['notes'])
    
    if data.get('external_order_id'):
        validated['external_order_id'] = str(data['external_order_id'])[:100]
    
    return len(errors) == 0, validated, errors
