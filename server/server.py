import socketio
import pymongo
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
import json

load_dotenv()

client = pymongo.MongoClient(os.getenv('DB_URI'))
# print(client.list_database_names())
db = client.TextEditor
table = db.Document


sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')

app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, environ):
    @sio.event
    async def getDocument(sid, documentId):
        document = findOrCreateDocument(documentId)
        doc=json.loads(document)
        sio.enter_room(sid,documentId)
        sio.emit('loadDocument',document["data"],to=sid)
        
        @sio.event
        async def sendChanges(sid,delta):
            sid.emit('receiveChanges',delta,room=documentId)
        
        @sio.event
        async def saveDocument(sid,data):
            table.update_one({"_id":ObjectId(documentId)},{"data":data})


@sio.event
async def disconnect(sid):
    print(sid, "disconnected")

defaultValue = ""


def findOrCreateDocument(id):
    if id is None:
        return
    document = table.find_one({"_id":ObjectId(id)})
    if document:
        return document
    return table.insert_one({"_id":ObjectId(id),"data":defaultValue})
