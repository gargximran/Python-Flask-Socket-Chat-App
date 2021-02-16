from marshmallow_mongoengine import ModelSchema

# import document
from ..documents.session_document import SessionDocument


class SessionSchema(ModelSchema):

    class Meta:
        model = SessionDocument
