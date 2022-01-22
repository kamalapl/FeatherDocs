import socketio
import pymongo
import os
from dotenv import load_dotenv
from engineio.payload import Payload

Payload.max_decode_packets = 100

load_dotenv()

client = pymongo.MongoClient(os.getenv('DB_URI'))
db = client.TextEditor
table = db.Document


sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, environ):
    print(sid, "connected")


@sio.event
async def getDocument(sid, documentId):

    await sio.save_session(sid, {'id': documentId})

    document = await findOrCreateDocument(documentId)

    await sio.emit('loadDocument', document['data'], to=sid)
    sio.enter_room(sid, documentId)


@sio.event
async def sendChanges(sid, delta):
    session = await sio.get_session(sid)
    await sio.emit('receiveChanges', delta, room=session['id'], skip_sid=sid)


@sio.event
async def saveDocument(sid, data):
    session = await sio.get_session(sid)

    query = {"_id": session['id']}
    change = {"$set": {"data": data}}
    table.update_one(query, change)


@sio.event
async def disconnect(sid):
    print(sid, "disconnected")


defaultValue = ""


async def findOrCreateDocument(id):
    if id is None:
        return
    document = table.find_one({"_id": id})

    if document:
        return document
    table.insert_one({"_id": id, "data": defaultValue})
    document = table.find_one({"_id": id})
    return document