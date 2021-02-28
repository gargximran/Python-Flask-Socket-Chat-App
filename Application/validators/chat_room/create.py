from flask import request


# import tools
from functools import wraps
from Application.helpers.response import Response

def validator(function):
    @wraps(function)
    def wrapper(*args, **kwargs):

        errors = {}

        if 'name' in request.values and request.values.get('name'):
            if len(request.values.get("name").strip()) < 2:
                errors.update({'name': 'Minimum 2 character required!'})
            if len(request.values.get('name').strip()) > 20:
                errors.update({'name': 'Maximum 20 character required!'})
        else:
            errors.update({'name': 'Name is required!'})

        if 'room_name' in request.values and request.values.get('room_name'):
            if len(request.values.get('room_name').strip()) < 2:
                errors.update({'room_name': 'Minimum 2 character required!'})
            if len(request.values.get('room_name').strip()) > 20:
                errors.update({"room_name": 'Maximum 20 character required!'})
        else:
            errors.update({'room_name': 'Room name is required!'})

        if len(errors) > 0:
            return Response(errors=errors, status_code=422, message='Invalid input!').send()
        return function(*args, **kwargs)
    return wrapper
