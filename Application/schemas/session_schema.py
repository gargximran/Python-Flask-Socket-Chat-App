from marshmallow_mongoengine import ModelSchema, fields

# import document
from ..documents.session_document import SessionDocument

# import schema
from .user_schema import User as UserSchema

class Session(ModelSchema):
    user = fields.Function(lambda obj: UserSchema().dump(obj.user).data) or None

    class Meta:
        model = SessionDocument
