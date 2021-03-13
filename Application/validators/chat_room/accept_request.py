from flask import request

# import tools
from functools import wraps
from bson.objectid import ObjectId

# import helpers
from Application.helpers.response import Response

# import document
from Application.documents.session_document import SessionDocument


def validator(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        errors = {}

        if 'request_member' in request.values and request.values.get('request_member'):
            if not ObjectId.is_valid(request.values.get('request_member')):
                errors.update({'request_member': 'Invalid id!'})
            else:
                member = SessionDocument.objects(
                    id=request.values.get('request_member')
                ).first()

                if not member:
                    errors.update({'request_member': 'Member not found!'})
        else:
            errors.update({'request_member': 'Field is required|!'})

        if len(errors) > 0:
            return Response(data=errors, status_code=422, message='Invalid input!').send()
        return function(*args, **kwargs)
    return wrapper
