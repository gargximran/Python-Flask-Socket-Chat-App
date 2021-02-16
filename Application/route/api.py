from . import register, get_routes

# import api controller files
from ..api.hello_world import hello_world


to = 'api'

def register_api_endpoints():
    """
    Define all api routes here
    :return:
    """
    register(endpoint='/hello_world', view_func=hello_world, to=to, prefix='api')


def fire_routes(blueprint):
    """
    :param blueprint: Blueprint
    :return:
    """
    routes = get_routes('api')
    for route in routes:
        endpoint = route['prefix'] and f"/{route['prefix']}{route['endpoint']}" or route['endpoint']
        blueprint.add_url_rule(endpoint, methods=route['methods'], view_func=route['view_func'])
