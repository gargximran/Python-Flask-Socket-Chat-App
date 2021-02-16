from mongoengine import Document, fields

# init session document
class SessionDocument(Document):
    user_agent = fields.StringField(required=True)
    name = fields.StringField(required=True)
    token = fields.StringField(required=True)
    created_at = fields.DateTimeField(required=True)

    meta = {
        'collection': 'sessions',
        'ordering': ['-created_at']
    }
