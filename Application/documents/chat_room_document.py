from mongoengine import fields, Document, signals

# import tools
from datetime import datetime, timedelta

# import documents
from .session_document import SessionDocument

class ChatRoomDocument(Document):
    name = fields.StringField(required=True)
    admin = fields.ReferenceField(document_type=SessionDocument, required=True)
    members = fields.ListField(fields.ReferenceField(document_type=SessionDocument))
    pending_members = fields.ListField(fields.ReferenceField(document_type=SessionDocument), required=False)
    created_at = fields.DateTimeField(required=False)
    expiration = fields.DateTimeField(required=False)

    meta = {
        'collection': 'chat_rooms',
        'ordering': ['-created_at']
    }

    @classmethod
    def set_timings(cls, sender, document, **kwargs):
        """
        Set Created and expiration at on Save
        :param sender:
        :param document:
        :param kwargs:
        :return:
        """
        document.created_at = datetime.utcnow()
        document.expiration = datetime.utcnow() + timedelta(minutes=30)


signals.pre_save.connect(ChatRoomDocument.set_timings)
