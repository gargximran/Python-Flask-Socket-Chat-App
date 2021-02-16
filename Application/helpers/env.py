envs = {
    "ENVIRONMENT": "development",
    "SECRET_KEY": "lskdgjgi8elik-52#",
    "MONGODB_SETTINGS": {
        'db': 'init'
    }
}

def get(key):
    """
    Get Environment Variables
    :param key: key
    :return: env value
    """
    return envs[key]
