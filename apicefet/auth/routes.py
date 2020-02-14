from flask import Blueprint
import apicefet.auth as auth

auth_bp = Blueprint('token', __name__)
auth_bp.add_url_rule('', 'user', auth.auth, methods=['POST'])
