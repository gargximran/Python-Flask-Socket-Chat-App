envs = {
    "ENVIRONMENT": "development",
    "SECRET_KEY": "secret-key",
    "MONGODB_SETTINGS": {
        'db': 'socket_chat_app'
    }
}

def get(key):
    """
    Get Environment Variables
    :param key: key
    :return: env value
    """
    return envs[key]
