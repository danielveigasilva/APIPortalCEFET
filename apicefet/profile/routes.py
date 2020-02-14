from flask import Blueprint
import apicefet.profile as profile

profile_bp = Blueprint('profile', __name__)
profile_bp.add_url_rule('', 'user', profile.perfilDados)
profile_bp.add_url_rule('/geral', 'geral', profile.perfilDadosGerais)
profile_bp.add_url_rule('/foto', 'photo', profile.perfilFoto)
