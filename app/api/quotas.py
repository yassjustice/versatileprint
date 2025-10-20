"""
Quota management API endpoints.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime

from app.services.quota_service import QuotaService
from app.utils.decorators import admin_required
from app.utils.helpers import build_error_response, build_success_response, parse_date

quotas_bp = Blueprint('quotas', __name__)


@quotas_bp.route('', methods=['GET'])
@login_required
def get_quota():
    """GET /api/quotas - Get quota information."""
    client_id = request.args.get('client_id', type=int)
    month_str = request.args.get('month')
    
    # Determine client_id
    if current_user.is_client:
        client_id = current_user.id
    elif not client_id and not current_user.is_admin:
        return jsonify(build_error_response('VALIDATION_ERROR', 'client_id required')[0]), 400
    
    # Parse month
    month = None
    if month_str:
        month = parse_date(month_str + '-01', '%Y-%m-%d')
        if not month:
            return jsonify(build_error_response('VALIDATION_ERROR', 'Invalid month format (use YYYY-MM)')[0]), 400
    
    # Get quota summary
    summary = QuotaService.get_quota_summary(client_id, month)
    
    return jsonify(build_success_response(summary)[0]), 200


@quotas_bp.route('/topup', methods=['POST'])
@login_required
@admin_required
def create_topup():
    """POST /api/quotas/topup - Create quota top-up (Admin only)."""
    data = request.get_json()
    
    if not data:
        return jsonify(build_error_response('VALIDATION_ERROR', 'Request body required')[0]), 400
    
    client_id = data.get('client_id')
    bw_added = data.get('bw_added', 0)
    color_added = data.get('color_added', 0)
    notes = data.get('notes')
    
    if not client_id:
        return jsonify(build_error_response('VALIDATION_ERROR', 'client_id required')[0]), 400
    
    success, topup, error = QuotaService.create_topup(
        client_id=client_id,
        admin_id=current_user.id,
        bw_added=bw_added,
        color_added=color_added,
        notes=notes
    )
    
    if not success:
        return jsonify(build_error_response('VALIDATION_ERROR', error)[0]), 400
    
    return jsonify(build_success_response(topup.to_dict(), 'Top-up created', 201)[0]), 201
