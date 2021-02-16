routes = {
    "api": []
}


def register(endpoint, view_func, methods=None, name=None, to='api', prefix=None):
    """
    Api Route Registration
    :param endpoint: str
    :param view_func: () -> Any
    :param methods: list
    :param name: str
    :param to: str
    :param prefix: str
    :return:
    """
    if methods is None:
        methods = ['GET', 'POST']

    routes[to].append(
        {
            'name': name,
            'endpoint': endpoint,
            'view_func': view_func,
            'methods': methods,
            'prefix': prefix
        }
    )

def get_routes(frm='api'):
    """
    Get Defined Api routes
    :param frm: str
    :return: routes
    """
    from .api import register_api_endpoints
    register_api_endpoints()
    return routes[frm]
