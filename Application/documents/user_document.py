from mongoengine import Document, fields, signals
from datetime import datetime


# init user document
class UserDocument(Document):
    name = fields.StringField(required=True)
    email = fields.EmailField(required=True)
    username = fields.StringField(required=True)

    active = fields.BooleanField()

    created_at = fields.DateTimeField(required=False)
    updated_at = fields.DateTimeField(required=False)

    meta = {
        'collection': 'users',
        'ordering': ['-created_at']
    }

    @classmethod
    def set_timings(cls, sender, document, **kwargs):
        """
        Set Created at on Save
        :param sender:
        :param document:
        :param kwargs:
        :return:
        """
        if 'created_at' not in kwargs and not document.created_at:
            document.created_at = datetime.utcnow()

    @classmethod
    def get_by_activation(cls, active=True):
        """
        Return All Active user
        :param active: Boolean
        :return UserDocument's:
        """
        return cls.objects(active=active)

    @classmethod
    def get_by_username(cls, username):
        """
        Return UserDocument by username
        :param username: String
        :return UserDocument:
        """
        return cls.objects(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        """
        Return UserDocument By Email
        :param email: String
        :return UserDocument:
        """
        cls.objects(email=email).first()


signals.pre_save.connect(UserDocument.set_timings)
