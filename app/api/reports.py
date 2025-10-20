"""
Reporting API endpoints (Admin only).
"""
from flask import Blueprint, request, jsonify, send_file
from flask_login import login_required
from datetime import datetime
import io

from app.utils.decorators import admin_required
from app.utils.helpers import build_error_response, build_success_response, parse_date

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/monthly', methods=['GET'])
@login_required
@admin_required
def monthly_report():
    """
    GET /api/reports/monthly - Export monthly report.
    Query params: month (YYYY-MM), format (csv|xlsx|pdf)
    """
    month_str = request.args.get('month')
    format_type = request.args.get('format', 'csv')
    
    if not month_str:
        return jsonify(build_error_response('VALIDATION_ERROR', 'month parameter required (YYYY-MM)')[0]), 400
    
    month = parse_date(month_str + '-01', '%Y-%m-%d')
    if not month:
        return jsonify(build_error_response('VALIDATION_ERROR', 'Invalid month format')[0]), 400
    
    # Placeholder for actual report generation
    # You would implement ReportService here
    
    if format_type == 'csv':
        # Generate CSV
        output = io.StringIO()
        output.write('Order ID,Client,B&W,Color,Status,Date\n')
        output.write('# Report data would go here\n')
        
        mem = io.BytesIO()
        mem.write(output.getvalue().encode('utf-8'))
        mem.seek(0)
        
        return send_file(
            mem,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'report_{month_str}.csv'
        )
    
    elif format_type == 'xlsx':
        return jsonify(build_error_response('NOT_IMPLEMENTED', 'Excel export not yet implemented')[0]), 501
    
    elif format_type == 'pdf':
        return jsonify(build_error_response('NOT_IMPLEMENTED', 'PDF export not yet implemented')[0]), 501
    
    else:
        return jsonify(build_error_response('VALIDATION_ERROR', 'Invalid format')[0]), 400
