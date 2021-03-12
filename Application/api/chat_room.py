from flask import request

# import sockets
from Application import socket


# import documents
from Application.documents.chat_room_document import ChatRoomDocument

# import schemas
from Application.schemas.room_schema import ChatRoomSchema
from Application.schemas.session_schema import SessionSchema

# import validators
from Application.validators.chat_room.create import validator as create_chat_room_validator
from Application.validators.chat_room.member_request import validator as new_member_request_validator

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
        chat_room_data = ChatRoomSchema().dump(chat_room).data
        session_data = SessionSchema().dump(session).data

        return Response(message='Chat room created!', session=session_data, data=chat_room_data).send()

    return Response(message='Something went wrong!', status_code=400).send()


@new_member_request_validator
def request_to_chat_room(room_id):
    room = ChatRoomDocument.objects(
        id=room_id
    ).first()

    if not room:
        return Response(status_code=404, message='Room not found!').send()

    session = set_current_session(request.values.get('name'))

    room.pending_members.append(session)
    if room.save():
        dump_session = SessionSchema().dump(session).data

        # emmit new socket request to room admin
        socket.emit(f'new member@{room.id}', ChatRoomSchema().dump(room.reload()).data, dump_session)

        return Response(data=dump_session).send()
    else:
        return Response(message='Something went wrong!', status_code=400).send()

