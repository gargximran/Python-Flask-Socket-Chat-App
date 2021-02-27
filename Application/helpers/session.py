# import request
from flask import request


# import documents
from ..documents.session_document import SessionDocument
from ..documents.chat_room_document import ChatRoomDocument

# import schema
from ..schemas.session_schema import SessionSchema

#  import utils
import hashlib
import datetime

def set_current_session(name=None):
    """
    Set session for current user
    :param user: UserDocument
    :return:
    """
    token = hashlib.sha256(
        request.user_agent.__str__().encode('utf-8') + datetime.datetime.utcnow().__str__().encode('utf-8') + name.encode('utf-8')
    ).hexdigest()

    session = SessionDocument(
        user_agent=request.user_agent.__str__(),
        name=name,
        token=token,
        created_at=datetime.datetime.utcnow(),
    ).save()
    return session

def get_current_session(formatted=True):
    """
    Get current session by auth token from header
    :param formatted: Boolean
    :return SessionDocument:
    """
    token = request.headers.get('auth-token')
    session = SessionDocument.objects(
        token=token,
        user_agent=request.user_agent.__str__()
    ).first()

    if session:
        # update room expiration
        update_current_room_expiration(session)
        
        if formatted:
            return SessionSchema(many=False).dump(session.reload).data
        return session

    return None


def delete_session(token):
    """
    Delete previous sessions for current user
    :param user: UserDocument
    :return:
    """
    sessions = SessionDocument.objects(
        token=token
    )
    sessions and sessions.delete()


def update_current_room_expiration(session):
    """
    Update current room expiration in every request
    :param session: SessionDocument
    :return:
    """

    chat_room = ChatRoomDocument.objects(
        members__contains=session
    ).first()
    chat_room.update(
        expiration=datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    )
