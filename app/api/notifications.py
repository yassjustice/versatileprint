"""
Notifications API endpoints.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app.models.notification import Notification
from app.utils.helpers import build_error_response, build_success_response, paginate_query_results

notifications_bp = Blueprint('notifications', __name__)


@notifications_bp.route('', methods=['GET'])
@login_required
def list_notifications():
    """GET /api/notifications - List user notifications."""
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    
    notifications = Notification.get_for_user(current_user.id, unread_only)
    notifications_data = [n.to_dict() for n in notifications]
    
    result = paginate_query_results(notifications_data, page, page_size)
    result['unread_count'] = Notification.count_unread(current_user.id)
    
    return jsonify(build_success_response(result)[0]), 200


@notifications_bp.route('/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_read(notification_id):
    """POST /api/notifications/:id/read - Mark notification as read."""
    notification = Notification.get_by_id(notification_id)
    
    if not notification:
        return jsonify(build_error_response('NOT_FOUND', 'Notification not found')[0]), 404
    
    if notification.user_id != current_user.id:
        return jsonify(build_error_response('PERMISSION_DENIED', 'Access forbidden')[0]), 403
    
    notification.mark_as_read()
    
    return jsonify(build_success_response(message='Notification marked as read')[0]), 200


@notifications_bp.route('/mark-all-read', methods=['POST'])
@login_required
def mark_all_read():
    """POST /api/notifications/mark-all-read - Mark all notifications as read."""
    Notification.mark_all_read(current_user.id)
    
    return jsonify(build_success_response(message='All notifications marked as read')[0]), 200
