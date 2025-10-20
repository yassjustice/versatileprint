"""
Application entry point.
Run this file to start the Flask development server.
"""
import os
from app import create_app

# Determine environment from FLASK_ENV or default to development
env = os.getenv('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    # Development server settings
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"Starting VersatilesPrint application in {env} mode...")
    print(f"Server running on http://{host}:{port}")
    
    app.run(host=host, port=port, debug=debug)
