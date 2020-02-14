from flask import Blueprint
import apicefet.profile as profile

profile_bp = Blueprint('profile', __name__)
profile_bp.add_url_rule('', 'user', profile.profile_data)
profile_bp.add_url_rule('/geral', 'geral', profile.profile_data_all)
profile_bp.add_url_rule('/foto', 'photo', profile.profile_photo)
