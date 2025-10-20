"""
Application factory and initialization.
Creates and configures the Flask application instance.
"""
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy          # 🧱 Added for Flask-Migrate
from flask_migrate import Migrate                # 🧱 Added for migrations
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

from config import config

# Initialize extensions
login_manager = LoginManager()
mail = Mail()

# 🧱 Added: SQLAlchemy db + migrate for ORM & migrations
db = SQLAlchemy()
migrate = Migrate()

# Database session (legacy style)
db_engine = None
db_session = None

def create_app(config_name='development'):
    """
    Application factory function.
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # 🧱 Initialize both ORM + manual connection
    init_database(app)
    
    # Initialize extensions
    init_extensions(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Create upload directories
    create_upload_dirs(app)
    
    # Context processors
    register_context_processors(app)
    
    return app

def init_database(app):
    """Initialize database connection and session."""
    global db_engine, db_session
    
    # 🧱 Flask-Migrate-compatible config
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Flask-SQLAlchemy
    db.init_app(app)
    
    # Initialize Flask-Migrate
    migrate.init_app(app, db)

    # Maintain your existing manual SQLAlchemy engine/session
    db_engine = create_engine(
        app.config['SQLALCHEMY_DATABASE_URI'],
        **app.config.get('SQLALCHEMY_ENGINE_OPTIONS', {})
    )
    session_factory = sessionmaker(bind=db_engine)
    db_session = scoped_session(session_factory)
    app.db_session = db_session
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

def init_extensions(app):
    """Initialize Flask extensions."""
    # Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'main.login_page'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'
    
    # Flask-Mail
    mail.init_app(app)
    
    # User loader for Flask-Login
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(int(user_id))

def register_blueprints(app):
    """Register application blueprints."""
    from app.api.auth import auth_bp
    from app.api.users import users_bp
    from app.api.orders import orders_bp
    from app.api.quotas import quotas_bp
    from app.api.csv_imports import csv_imports_bp
    from app.api.notifications import notifications_bp
    from app.api.reports import reports_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(quotas_bp, url_prefix='/api/quotas')
    app.register_blueprint(csv_imports_bp, url_prefix='/api/csv-imports')
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    
    from app.views import main
    app.register_blueprint(main)

def register_error_handlers(app):
    """Register error handlers."""
    from flask import jsonify, render_template, request
    
    @app.errorhandler(400)
    def bad_request(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': {'code': 'BAD_REQUEST', 'message': 'Bad request', 'details': str(error)}}), 400
        return render_template('errors/400.html'), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': {'code': 'UNAUTHORIZED', 'message': 'Authentication required', 'details': str(error)}}), 401
        return render_template('errors/401.html'), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': {'code': 'PERMISSION_DENIED', 'message': 'Access forbidden', 'details': str(error)}}), 403
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Resource not found', 'details': str(error)}}), 404
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': {'code': 'INTERNAL_ERROR', 'message': 'Internal server error', 'details': str(error) if app.debug else 'An error occurred'}}), 500
        return render_template('errors/500.html'), 500

def create_upload_dirs(app):
    """Create upload directories if they don't exist."""
    upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads/csv')
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs('logs', exist_ok=True)

def register_context_processors(app):
    """Register template context processors."""
    from datetime import datetime
    
    @app.context_processor
    def utility_processor():
        return {'now': datetime.utcnow, 'app_name': 'VersatilesPrint'}
