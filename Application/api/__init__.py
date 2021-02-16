from flask import Blueprint

# import routes
from Application.route.api import fire_routes as fire_api_routes

api = Blueprint('data', __name__)

fire_api_routes(api)
