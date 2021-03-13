from flask import request

# import sockets
from Application import socket


# import documents
from Application.documents.chat_room_document import ChatRoomDocument
from Application.documents.session_document import SessionDocument

# import schemas
from Application.schemas.room_schema import ChatRoomSchema
from Application.schemas.session_schema import SessionSchema

# import validators
from Application.validators.chat_room.create import validator as create_chat_room_validator
from Application.validators.chat_room.member_request import validator as new_member_request_validator
from Application.validators.chat_room.accept_request import validator as accept_request_validator

# import helpers
from Application.helpers.session import set_current_session
from Application.helpers.response import Response

# import tools
from bson.objectid import ObjectId


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
    if not ObjectId.is_valid(room_id):
        return Response(status_code=404, message='Invalid url!').send()

    room = ChatRoomDocument.objects(
        id=room_id
    ).first()

    if not room:
        return Response(status_code=404, message='Room not found!').send()

    session = set_current_session(request.values.get('name'))

    room.pending_members.append(session)
    if room.save():
        dump_session = SessionSchema().dump(session).data
        dump_chat_room = ChatRoomSchema().dump(room.reload()).data

        # emmit new socket request to room admin
        socket.emit(f'new member@{room.id}', dump_chat_room, dump_session, namespace='/request')

        return Response(data=dump_session).send()

    return Response(message='Something went wrong!', status_code=400).send()


@accept_request_validator
def accept_pending_request(room_id):
    if not ObjectId.is_valid(room_id):
        return Response(status_code=404, message='Invalid request').send()

    room = ChatRoomDocument.objects(
        id=room_id
    ).first()

    request_member = SessionDocument.objects(
        id=request.values.get('request_member')
    ).first()

    if request_member not in room.pending_members:
        return Response(status_code=404, message='Member not found!').send()

    room.pending_members.remove(request_member)
    room.members.append(request_member)

    if room.save():
        dump_room = ChatRoomSchema().dump(room.reload()).data

        # socket send to room
        socket.emit(f'request approved@{room.id}', dump_room)

        # socket send to requested member
        socket.emit(f'request approved@{request_member.id}', dump_room)

        return Response(message='New member approved to room!', data=dump_room).send()

    return Response(message='Something went wrong!', status_code=400).send()
