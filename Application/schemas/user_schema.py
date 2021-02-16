from marshmallow_mongoengine import ModelSchema

# import document
from ..documents.user_document import UserDocument

class User(ModelSchema):

    class Meta:
        model = UserDocument
        exclude = ['created_at']

