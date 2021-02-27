from flask import request


# import documents
from Application.documents.chat_room_document import ChatRoomDocument

# import schemas
from Application.schemas.room_schema import ChatRoomSchema
from Application.schemas.session_schema import SessionSchema

# import validators
from Application.validators.chat_room.create import validator as create_chat_room_validator

# import helpers
from Application.helpers.session import set_current_session
from Application.helpers.response import Response


@create_chat_room_validator
def create_chat_room():
    values = request.values

    session = set_current_session(values.get('name'))

    chat_room = ChatRoomDocument(
        name=values.get('room_name'),
        admin=session
    )

    chat_room.members.append(session)

    if chat_room.save():
        return Response(message='Chat room created!', session=SessionSchema().dump(session).data, data=ChatRoomSchema().dump(chat_room).data).send()

    return Response(message='Something went wrong!', status_code=400).send()


