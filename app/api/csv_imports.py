"""
CSV import API endpoints (Admin only).
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app.services.csv_service import CSVService
from app.models.csv_import import CSVImport
from app.utils.decorators import admin_required
from app.utils.helpers import build_error_response, build_success_response

csv_imports_bp = Blueprint('csv-imports', __name__)


@csv_imports_bp.route('', methods=['GET'])
@login_required
@admin_required
def list_imports():
    """GET /api/csv-imports - List CSV imports."""
    imports = CSVImport.get_all()
    imports_data = [i.to_dict(include_relations=True) for i in imports]
    
    return jsonify(build_success_response({'items': imports_data})[0]), 200


@csv_imports_bp.route('', methods=['POST'])
@login_required
@admin_required
def upload_csv():
    """POST /api/csv-imports - Upload CSV file."""
    if 'file' not in request.files:
        return jsonify(build_error_response('VALIDATION_ERROR', 'No file provided')[0]), 400
    
    file = request.files['file']
    
    success, csv_import, error = CSVService.upload_csv(file, current_user.id)
    
    if not success:
        return jsonify(build_error_response('VALIDATION_ERROR', error)[0]), 400
    
    return jsonify(build_success_response(csv_import.to_dict(), 'File uploaded', 201)[0]), 201


@csv_imports_bp.route('/<int:import_id>', methods=['GET'])
@login_required
@admin_required
def get_import(import_id):
    """GET /api/csv-imports/:id - Get import details with preview."""
    csv_import = CSVImport.get_by_id(import_id)
    if not csv_import:
        return jsonify(build_error_response('NOT_FOUND', 'Import not found')[0]), 404
    
    # Parse and validate for preview
    success, validation_result, error = CSVService.parse_and_validate_csv(import_id)
    
    if not success:
        return jsonify(build_error_response('VALIDATION_ERROR', error)[0]), 400
    
    result = {
        'import': csv_import.to_dict(include_relations=True),
        'validation': validation_result
    }
    
    return jsonify(build_success_response(result)[0]), 200


@csv_imports_bp.route('/<int:import_id>/validate', methods=['POST'])
@login_required
@admin_required
def validate_import(import_id):
    """POST /api/csv-imports/:id/validate - Validate and import CSV."""
    data = request.get_json() or {}
    corrections = data.get('corrections', {})
    
    success, result, error = CSVService.validate_and_import(import_id, current_user.id, corrections)
    
    if not success:
        return jsonify(build_error_response('VALIDATION_ERROR', error)[0]), 400
    
    return jsonify(build_success_response(result, 'Import validated and processed')[0]), 200


@csv_imports_bp.route('/<int:import_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_import(import_id):
    """POST /api/csv-imports/:id/reject - Reject CSV import."""
    data = request.get_json()
    
    if not data or not data.get('notes'):
        return jsonify(build_error_response('VALIDATION_ERROR', 'Rejection notes required')[0]), 400
    
    success, error = CSVService.reject_import(import_id, current_user.id, data['notes'])
    
    if not success:
        return jsonify(build_error_response('VALIDATION_ERROR', error)[0]), 400
    
    return jsonify(build_success_response(message='Import rejected')[0]), 200
