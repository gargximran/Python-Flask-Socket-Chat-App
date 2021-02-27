from mongoengine import fields, Document, signals

# import documents
from .session_document import SessionDocument
from .chat_room_document import ChatRoomDocument

# import tools
from datetime import datetime


class MessageDocument(Document):
    text = fields.StringField(required=False)
    images = fields.ListField(fields.ImageField(collection_name='message_images'), required=False)
    document = fields.FileField(collection_name='message_documents', required=False)
    session = fields.ReferenceField(document_type=SessionDocument, required=True)
    room = fields.ReferenceField(document_type=ChatRoomDocument, required=True)
    seen_by = fields.ListField(fields.ReferenceField(document_type=SessionDocument), required=False)
    created_at = fields.DateTimeField(required=False)

    meta = {
        'collection': 'messages',
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


signals.pre_save.connect(MessageDocument.set_timings)
