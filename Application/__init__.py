# Import Flask Things
from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine

# import Helpers
from Application.helpers import env

# import error handler
from .errors import handle_404_errors, handle_500_errors


# app fire
def create_app(debug=False):
    """Create an application"""
    app = Flask(__name__)
    app.debug = debug

    # app configuration's
    app.config['SECRET_KEY'] = env.get('SECRET_KEY')
    app.config['MONGODB_SETTINGS'] = env.get('MONGODB_SETTINGS')

    MongoEngine(app)
    CORS(app)

    # error handling
    app.register_error_handler(404, handle_404_errors)
    app.register_error_handler(500, handle_500_errors)

    # register blueprint
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app




