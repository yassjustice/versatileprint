"""
Web views blueprint for HTML pages.
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

# Create blueprint with 'main' name for url_for references
main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Landing page."""
    return render_template('public/index.html')


@main.route('/dashboard')
@login_required
def dashboard():
    """User dashboard (role-based)."""
    # Single dashboard template with role-based content
    return render_template('dashboard.html')


@main.route('/login')
def login_page():
    """Login page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('auth/login.html')


@main.route('/profile')
@login_required
def profile():
    """User profile page."""
    return render_template('auth/profile.html')


@main.route('/reports')
@login_required
def reports():
    """Reports and analytics page."""
    return render_template('reports.html')
