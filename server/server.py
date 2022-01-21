import socketio
import pymongo
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
from engineio.payload import Payload

Payload.max_decode_packets = 100

load_dotenv()

client = pymongo.MongoClient(os.getenv('DB_URI'))
# print(client.list_database_names())
db = client.TextEditor
table = db.Document


sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')

app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, environ):
    print(sid,"connected")

@sio.event
async def getDocument(sid, documentId):
    #id = authenticate_user(documentId)
    await sio.save_session(sid, {'id': documentId})
    oid=documentId
    document =await findOrCreateDocument(documentId)
    print()
    print()
    print(type(document))
    print(document)
    d=(str(document)).replace("\'","\"")
    print(d)
    doc=loads(d)
    print(doc)
    print(type(doc))
    
    await sio.emit('loadDocument',doc["data"],to=sid)
    sio.enter_room(sid,documentId)
        
@sio.event
async def sendChanges(sid,delta):
    session = await sio.get_session(sid)
    await sio.emit('receiveChanges',delta,room=session['id'],skip_sid=sid)
        
@sio.event
async def saveDocument(sid,data):
    print("saving id")
    #print(oid)
    print(data)
    session = await sio.get_session(sid)
    print("session")
    print(session)
    #print('message from ', session['username'])
    query={"_id":session['id']}
    change={"$set":{"data":data}}
    table.update_one(query,change)


@sio.event
async def disconnect(sid):
    print(sid, "disconnected")

defaultValue = ""


async def findOrCreateDocument(id):
    if id is None:
        return
    document = table.find_one({"_id":id})
    if document:
        print("aaa")
        print(document)
        return document
    print("bbb")
    table.insert_one({"_id":id,"data":defaultValue})
    document = table.find_one({"_id":id})
    return document
