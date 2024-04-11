from flask import Blueprint
from src.controllers.user_controller import handle_signup, handle_login

#blueprint for Authentication 
auth_bp = Blueprint('auth_bp', __name__)
auth_bp.route('/signin', methods=['POST'])(handle_login)
auth_bp.route('/signup', methods=['POST'])(handle_signup)
