from mongoengine import Document, fields, signals

# import documents
from .user_document import UserDocument

# init session document
class SessionDocument(Document):
    user_agent = fields.StringField(required=True)
    user = fields.ReferenceField(document_type=UserDocument, required=True)
    expiration = fields.DateTimeField(required=True)
    token = fields.StringField(required=True)
    created_at = fields.DateTimeField(required=True)

    meta = {
        'collection': 'sessions',
        'ordering': ['-created_at']
    }
