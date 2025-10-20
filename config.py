"""
Application configuration module.
Loads environment variables and provides config classes for different environments.
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration with common settings."""
    
    # Flask core
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:password@localhost:3306/versatiles_print')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20
    }
    
    # Mail configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@versatiles.com')
    
    # Agent workload
    MAX_ACTIVE_ORDERS_DEFAULT = int(os.getenv('MAX_ACTIVE_ORDERS_DEFAULT', 10))
    MAX_ACTIVE_ORDERS_OVERRIDE = int(os.getenv('MAX_ACTIVE_ORDERS_OVERRIDE', 30))
    
    # Validation patterns
    PHONE_VALIDATION_PATTERN = os.getenv('PHONE_VALIDATION_PATTERN', r'^\+?[1-9]\d{1,14}$')
    CSV_IDEMPOTENCY_MODE = os.getenv('CSV_IDEMPOTENCY_MODE', 'reject')  # reject | skip | upsert
    
    # Quota settings
    QUOTA_WARNING_THRESHOLD = float(os.getenv('QUOTA_WARNING_THRESHOLD', 0.8))
    DEFAULT_BW_LIMIT = int(os.getenv('DEFAULT_BW_LIMIT', 3000))
    DEFAULT_COLOR_LIMIT = int(os.getenv('DEFAULT_COLOR_LIMIT', 2000))
    MIN_TOPUP_AMOUNT = int(os.getenv('MIN_TOPUP_AMOUNT', 1000))
    
    # File uploads
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads/csv')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    ALLOWED_EXTENSIONS = {'csv'}
    
    # Session
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=int(os.getenv('PERMANENT_SESSION_LIFETIME', 3600)))
    
    # Timezone
    TIMEZONE = os.getenv('TIMEZONE', 'UTC')
    
    # Pagination
    DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE', 20))
    MAX_PAGE_SIZE = int(os.getenv('MAX_PAGE_SIZE', 100))
    
    # Security
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
