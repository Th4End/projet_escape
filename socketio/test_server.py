import socketio
from aiohttp import web

sio = socketio.AsyncServer(cors_allowed_origins="*")
app = web.Application()
sio.attach(app)

@sio.event
async def connect(sid, environ):
    print("Client connected:", sid)
    await sio.emit('message', {'data': 'Welcome!'}, to=sid)
    
@sio.event
async def disconnect(sid):
    print("Client disconnected:", sid)
    
@sio.event
async def join_game(sid, data):
    print(f"User {data['username']} with role {data['role']} joined the game.")
    await sio.emit('user_joined', data)

@sio.event
async def action(sid, data):
    print(f"Action received from {sid}: {data}")
    await sio.emit('action_response', {'status': 'Action received'}, to=sid)
    
if __name__ == '__main__':
    web.run_app(app, port=5000)