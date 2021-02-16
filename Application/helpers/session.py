# import request
from flask import request


# import documents
from ..documents.user_document import UserDocument
from ..documents.session_document import SessionDocument

# import schema
from ..schemas.session_schema import Session as SessionSchema

#  import utils
import hashlib
import datetime

def set_current_session(user=None):
    """
    Set session for current user
    :param user: UserDocument
    :return:
    """
    token = hashlib.sha256(
        request.user_agent.__str__().encode('utf-8') + datetime.datetime.utcnow().__str__().encode("utf-8") + str(user.id).encode('utf-8')
    )

    # Delete prev sessions
    delete_prev_session(user)

    session = SessionDocument(
        user_agent=request.user_agent.__str__(),
        user=user,
        expiration=datetime.datetime.utcnow() + datetime.timedelta(hours=48),
        token=token,
        created_at=datetime.datetime.utcnow()
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
        user_agent=request.user_agent.__str__(),
        expiration__gte=datetime.datetime.utcnow()
    ).first()

    if session:
        # update current session
        update_token_expiration(session)
        if formatted:
            return SessionSchema.dump(session.reload).data
        return session

    return None

def get_current_user():
    """
    Get current user
    :return UserDocument:
    """
    current_session = get_current_session(formatted=False)
    return current_session and current_session.user

def update_token_expiration(session):
    """
    update token expiration
    :param session: SessionDocument
    :return:
    """
    session.update(
        expiration=datetime.datetime.utcnow() + datetime.timedelta(hours=48)
    )


def delete_prev_session(user):
    """
    Delete previous sessions for current user
    :param user: UserDocument
    :return:
    """
    sessions = SessionDocument.objects(
        user=user
    )
    sessions and sessions.delete()



