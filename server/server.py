import socketio

sio = socketio.AsyncServer(cors_allowed_origins='*',async_mode='asgi')

app=socketio.ASGIApp(sio)

@sio.event
async def connect(sid,environ):
    print(sid,"connected")

@sio.event
async def disconnect(sid):
    print(sid,"disconnected")
