from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


def http_exception_handler(error):
    return jsonify({
        "code": error.code,
        "error": error.description
    })


def create_app():
    app = Flask(__name__)

    # Init configs
    # Init extensions

    with app.app_context():
        from apicefet.auth.routes import auth_bp
        from apicefet.profile.routes import profile_bp
        from apicefet.reports.routes import reports_bp
        from apicefet.schedule.routes import schedule_bp

        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(profile_bp, url_prefix='/perfil')
        app.register_blueprint(reports_bp, url_prefix='/relatorios')
        app.register_blueprint(schedule_bp, url_prefix='/horarios')

        app.register_error_handler(HTTPException, http_exception_handler)

    return app
