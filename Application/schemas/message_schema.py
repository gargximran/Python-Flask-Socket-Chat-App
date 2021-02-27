from marshmallow_mongoengine import ModelSchema, fields

# import document
from Application.documents.message_document import MessageDocument

# import schema
from Application.schemas.session_schema import SessionSchema

class MessageSchema(ModelSchema):
    session = fields.Function(lambda obj: SessionSchema(many=False).dump(obj.session).data)

    class Meta:
        model = MessageDocument
