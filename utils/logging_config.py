import os
import logging
from logging.handlers import RotatingFileHandler
from flask import request

# Configure logging
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

class SecurityFilter(logging.Filter):
    def filter(self, record):
        return 'security' in record.getMessage().lower()

# Set up logging configuration
def setup_logging(app):
    # Main application logger
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Regular application logs
    app_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, 'app.log'),
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    app_handler.setFormatter(formatter)
    app_handler.setLevel(logging.INFO)
    
    # Security-specific logs
    security_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, 'security.log'),
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    security_handler.setFormatter(formatter)
    security_handler.setLevel(logging.WARNING)
    security_handler.addFilter(SecurityFilter())
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(app_handler)
    root_logger.addHandler(security_handler)
    
    # Werkzeug logger (for request/response logs)
    logging.getLogger('werkzeug').setLevel(logging.INFO)
    
    # Add security logging to app
    @app.after_request
    def log_request_info(response):
        if response.status_code >= 400:
            app.logger.warning(
                f'Request: {request.method} {request.url} - Status: {response.status_code}'
                f' - IP: {request.remote_addr}'
            )
        return response

    return app