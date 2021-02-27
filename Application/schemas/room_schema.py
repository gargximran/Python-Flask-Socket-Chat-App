from marshmallow_mongoengine import ModelSchema, fields

# import document
from Application.documents.chat_room_document import ChatRoomDocument

# import schemas
from Application.schemas.session_schema import SessionSchema

class ChatRoomSchema(ModelSchema):
    admin = fields.Function(lambda obj: SessionSchema(many=False).dump(obj.admin).data)
    members = fields.Function(lambda obj: SessionSchema(many=True).dump(obj.members).data)
    pending_members = fields.Function(lambda obj: SessionSchema(many=True).dump(obj.pending_members).data)

    class Meta:
        model = ChatRoomDocument
        exclude = ['expiration']
