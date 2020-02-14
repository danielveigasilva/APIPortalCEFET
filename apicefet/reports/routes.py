from flask import Blueprint
import apicefet.reports as reports

reports_bp = Blueprint('reports', __name__)
reports_bp.add_url_rule('', 'list', reports.lista_relatorios)
reports_bp.add_url_rule('/<path:url>', 'generate', reports.geraRelatorio)
