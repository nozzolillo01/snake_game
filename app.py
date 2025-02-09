from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from database import init_db
from routes.dashboard import dashboard
from routes.game import game
from config import config
from utils.logging_config import setup_logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

def create_app(config_name='development'):
    app = Flask(__name__, static_folder='static')
    app.config.from_object(config[config_name])

    # Initialize extensions
    CORS(app)
    socketio = SocketIO(app, cors_allowed_origins="*")
    limiter.init_app(app)

    # Setup logging
    app = setup_logging(app)

    # Initialize database
    init_db()

    # Register blueprints
    app.register_blueprint(dashboard)
    app.register_blueprint(game)

    # Security headers middleware
    @app.after_request
    def add_security_headers(response):
        response.headers.update({
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'SAMEORIGIN',
            'X-XSS-Protection': '1; mode=block',
            'Content-Security-Policy': "default-src 'self' 'unsafe-inline' 'unsafe-eval' https://fonts.googleapis.com https://fonts.gstatic.com",
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'X-Permitted-Cross-Domain-Policies': 'none',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0'
        })
        return response

    @app.errorhandler(429)
    def ratelimit_handler(e):
        app.logger.warning(f'Rate limit exceeded by IP: {request.remote_addr}')
        return {"error": "Rate limit exceeded", "message": str(e.description)}, 429

    @app.errorhandler(500)
    def internal_error(e):
        app.logger.error(f'Internal Server Error: {str(e)}')
        return {"error": "Internal Server Error"}, 500

    return app, socketio

app, socketio = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    socketio.run(app, debug=app.config['DEBUG'])