
from flask import Blueprint
from src.routes.auth_bp import auth_bp

# Main blueprint to be registered with the application
api = Blueprint('api', __name__)

# Register auth blueprint with api blueprint
api.register_blueprint(auth_bp, url_prefix="/auth")
