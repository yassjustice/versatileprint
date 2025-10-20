"""
CSV import and validation service.
Handles CSV file processing, validation, and bulk order creation.
"""
import csv
import os
from typing import Tuple, Optional, List, Dict, Any
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app

from app.models.csv_import import CSVImport, CSVImportStatus
from app.models.user import User
from app.models.audit_log import AuditLog
from app.services.order_service import OrderService
from app.utils.helpers import generate_secure_filename, ensure_directory_exists
from app.utils.validators import validate_csv_row_data, validate_email, validate_phone


class CSVService:
    """CSV import and validation service."""
    
    @staticmethod
    def upload_csv(file, uploaded_by_id: int) -> Tuple[bool, Optional[CSVImport], Optional[str]]:
        """
        Upload and store CSV file.
        
        Args:
            file: Uploaded file object
            uploaded_by_id: Admin user ID uploading
        
        Returns:
            (success, csv_import, error_message)
        """
        try:
            # Validate file
            if not file or file.filename == '':
                return False, None, 'No file selected'
            
            if not file.filename.endswith('.csv'):
                return False, None, 'File must be a CSV file'
            
            # Generate secure filename
            original_filename = secure_filename(file.filename)
            stored_filename = generate_secure_filename(original_filename, prefix='import')
            
            # Ensure upload directory exists
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads/csv')
            ensure_directory_exists(upload_folder)
            
            # Save file
            filepath = os.path.join(upload_folder, stored_filename)
            file.save(filepath)
            
            # Create CSV import record
            csv_import = CSVImport(
                uploaded_by=uploaded_by_id,
                original_filename=original_filename,
                stored_filepath=filepath,
                status=CSVImportStatus.PENDING_VALIDATION
            )
            csv_import.save()
            
            # Log upload
            AuditLog.log_action(
                action='CSV_UPLOADED',
                user_id=uploaded_by_id,
                details={
                    'import_id': csv_import.id,
                    'filename': original_filename
                }
            )
            
            return True, csv_import, None
            
        except Exception as e:
            return False, None, f'Failed to upload CSV: {str(e)}'
    
    @staticmethod
    def parse_and_validate_csv(import_id: int) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Parse and validate CSV file.
        
        Args:
            import_id: CSV import ID
        
        Returns:
            (success, validation_result, error_message)
        """
        try:
            # Get CSV import
            csv_import = CSVImport.get_by_id(import_id)
            if not csv_import:
                return False, None, 'CSV import not found'
            
            if not os.path.exists(csv_import.stored_filepath):
                return False, None, 'CSV file not found'
            
            # Parse CSV
            rows = []
            errors = []
            valid_count = 0
            error_count = 0
            external_ids_seen = set()
            
            with open(csv_import.stored_filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row_num, row in enumerate(reader, start=2):  # Start at 2 (after header)
                    row_data = {k.strip(): v.strip() for k, v in row.items()}
                    row_errors = []
                    
                    # Basic validation
                    is_valid, validation_errors = validate_csv_row_data(row_data, row_num)
                    if not is_valid:
                        row_errors.extend(validation_errors)
                    
                    # Validate client exists
                    client = None
                    if row_data.get('client_id'):
                        client = User.get_by_id(int(row_data['client_id']))
                        if not client or not client.is_client:
                            row_errors.append(f'Row {row_num}: Invalid client_id')
                    elif row_data.get('client_email'):
                        client = User.get_by_email(row_data['client_email'])
                        if not client or not client.is_client:
                            row_errors.append(f'Row {row_num}: Client email not found')
                    
                    # Validate agent if provided
                    agent = None
                    if row_data.get('agent_id'):
                        agent = User.get_by_id(int(row_data['agent_id']))
                        if not agent or not agent.is_agent:
                            row_errors.append(f'Row {row_num}: Invalid agent_id')
                    elif row_data.get('agent_email'):
                        agent = User.get_by_email(row_data['agent_email'])
                        if not agent or not agent.is_agent:
                            row_errors.append(f'Row {row_num}: Agent email not found')
                    
                    # Check for duplicate external_order_id within file
                    external_id = row_data.get('external_order_id')
                    if external_id:
                        if external_id in external_ids_seen:
                            row_errors.append(f'Row {row_num}: Duplicate external_order_id within file')
                        else:
                            external_ids_seen.add(external_id)
                            
                            # Check if exists in database
                            from app.models.order import Order
                            existing_order = Order.get_by_external_id(external_id)
                            if existing_order:
                                row_errors.append(f'Row {row_num}: external_order_id already exists in database (Order #{existing_order.id})')
                    
                    # Normalize phone if provided
                    normalized_phone = None
                    if row_data.get('client_phone'):
                        pattern = current_app.config.get('PHONE_VALIDATION_PATTERN')
                        phone_valid, normalized_phone, phone_error = validate_phone(row_data['client_phone'], pattern)
                        if not phone_valid:
                            row_errors.append(f'Row {row_num}: {phone_error}')
                    
                    # Build row result
                    row_result = {
                        'row_number': row_num,
                        'data': row_data,
                        'client_id': client.id if client else None,
                        'agent_id': agent.id if agent else None,
                        'normalized_phone': normalized_phone,
                        'errors': row_errors,
                        'is_valid': len(row_errors) == 0
                    }
                    
                    rows.append(row_result)
                    
                    if row_result['is_valid']:
                        valid_count += 1
                    else:
                        error_count += 1
                        errors.extend(row_errors)
            
            # Update CSV import record
            csv_import.row_count = len(rows)
            csv_import.valid_rows = valid_count
            csv_import.error_rows = error_count
            csv_import.save()
            
            result = {
                'import_id': import_id,
                'total_rows': len(rows),
                'valid_rows': valid_count,
                'error_rows': error_count,
                'rows': rows,
                'errors': errors
            }
            
            return True, result, None
            
        except Exception as e:
            return False, None, f'Failed to parse CSV: {str(e)}'
    
    @staticmethod
    def validate_and_import(import_id: int, validated_by_id: int, corrections: Dict[int, Dict] = None) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Validate and import CSV data as orders.
        
        Args:
            import_id: CSV import ID
            validated_by_id: Admin user ID validating
            corrections: Optional corrections dict {row_number: corrected_data}
        
        Returns:
            (success, result_dict, error_message)
        """
        try:
            # Parse and validate
            success, validation_result, error = CSVService.parse_and_validate_csv(import_id)
            if not success:
                return False, None, error
            
            # Apply corrections if provided
            if corrections:
                for row_num, corrected_data in corrections.items():
                    for row in validation_result['rows']:
                        if row['row_number'] == row_num:
                            row['data'].update(corrected_data)
                            # Re-validate corrected row
                            is_valid, _ = validate_csv_row_data(row['data'], row_num)
                            row['is_valid'] = is_valid
                            break
            
            # Count valid rows after corrections
            valid_rows = [r for r in validation_result['rows'] if r['is_valid']]
            
            if len(valid_rows) == 0:
                return False, None, 'No valid rows to import'
            
            # Import valid rows as orders
            imported_orders = []
            import_errors = []
            
            for row in valid_rows:
                data = row['data']
                
                # Create order
                order_success, order, order_error = OrderService.create_order(
                    client_id=row['client_id'],
                    bw_quantity=int(data.get('bw_quantity', 0)),
                    color_quantity=int(data.get('color_quantity', 0)),
                    paper_dimensions=data.get('paper_dimensions'),
                    paper_type=data.get('paper_type'),
                    finishing=data.get('finishing'),
                    notes=data.get('notes'),
                    agent_id=row.get('agent_id'),
                    external_order_id=data.get('external_order_id'),
                    import_id=import_id,
                    created_by_id=validated_by_id
                )
                
                if order_success:
                    imported_orders.append(order.id)
                else:
                    import_errors.append(f"Row {row['row_number']}: {order_error}")
            
            # Get CSV import
            csv_import = CSVImport.get_by_id(import_id)
            
            # Mark as validated
            csv_import.mark_validated(
                validated_by_id=validated_by_id,
                valid_count=len(imported_orders),
                error_count=len(import_errors),
                notes=f"Imported {len(imported_orders)} orders. Errors: {len(import_errors)}"
            )
            
            # Log action
            AuditLog.log_action(
                action='CSV_VALIDATED',
                user_id=validated_by_id,
                details={
                    'import_id': import_id,
                    'imported_orders': len(imported_orders),
                    'errors': len(import_errors)
                }
            )
            
            # Send notification
            from app.services.notification_service import NotificationService
            message = f"CSV Import #{import_id} validated: {len(imported_orders)} orders created"
            if import_errors:
                message += f", {len(import_errors)} errors"
            NotificationService.create_csv_notification(
                admin_id=validated_by_id,
                import_id=import_id,
                status='validated',
                message=message
            )
            
            result = {
                'import_id': import_id,
                'imported_orders': imported_orders,
                'import_errors': import_errors,
                'success_count': len(imported_orders),
                'error_count': len(import_errors)
            }
            
            return True, result, None
            
        except Exception as e:
            return False, None, f'Failed to import CSV: {str(e)}'
    
    @staticmethod
    def reject_import(import_id: int, rejected_by_id: int, notes: str) -> Tuple[bool, Optional[str]]:
        """
        Reject CSV import.
        
        Args:
            import_id: CSV import ID
            rejected_by_id: Admin user ID rejecting
            notes: Rejection notes
        
        Returns:
            (success, error_message)
        """
        try:
            csv_import = CSVImport.get_by_id(import_id)
            if not csv_import:
                return False, 'CSV import not found'
            
            csv_import.mark_rejected(rejected_by_id, notes)
            
            # Log action
            AuditLog.log_action(
                action='CSV_REJECTED',
                user_id=rejected_by_id,
                details={
                    'import_id': import_id,
                    'notes': notes
                }
            )
            
            # Send notification
            from app.services.notification_service import NotificationService
            NotificationService.create_csv_notification(
                admin_id=csv_import.uploaded_by,
                import_id=import_id,
                status='rejected',
                message=f"CSV Import #{import_id} was rejected: {notes}"
            )
            
            return True, None
            
        except Exception as e:
            return False, str(e)
