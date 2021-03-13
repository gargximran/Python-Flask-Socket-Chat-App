from . import register, get_routes

# import api controller files
from ..api.chat_room import create_chat_room, request_to_chat_room, accept_pending_request


to = 'api'

def register_api_endpoints():
    """
    Define all api routes here
    :return:
    """
    register(endpoint='/create_room', view_func=create_chat_room, to=to, prefix='api', methods=['POST'])
    register(endpoint='/request/<room_id>', view_func=request_to_chat_room, to=to, prefix='api', methods=['POST'])
    register(endpoint='/accept_member/<room_id>', view_func=accept_pending_request, to=to, prefix='api', methods=['POST'])



def fire_routes(blueprint):
    """
    :param blueprint: Blueprint
    :return:
    """
    routes = get_routes('api')
    for route in routes:
        endpoint = route['prefix'] and f"/{route['prefix']}{route['endpoint']}" or route['endpoint']
        blueprint.add_url_rule(endpoint, methods=route['methods'], view_func=route['view_func'])
