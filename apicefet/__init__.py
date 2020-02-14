from flask import Flask


def create_app():
    app = Flask(__name__)

    # Init configs
    # Init extensions

    with app.app_context():
        # Register blueprints
        pass

    return app
