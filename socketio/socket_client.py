import socketio

class SocketClient:
    def __init__(self, server_url, debug=False):
        self.sio = socketio.AsyncClient(
            logger=debug,
            engineio_logger=debug,
        )
        self.server_url = server_url
    
        @self.sio.event
        async def connect():
            print("Connected to server")

        @self.sio.event
        async def disconnect():
            print("Disconnected from server")
            
        @self.sio.event
        async def connect_error(data):
            print("Connection failed:", data)
            
        @self.sio.event
        async def message(data):
            print("Message received:", data)
            
        @self.sio.event
        async def game_update(data):
            print("Game update received:", data)
        
        @self.sio.event
        async def puzzle_solved(data):
            print("Puzzle solved:", data)

    async def connect(self):
        await self.sio.connect(self.server_url)

    async def send_message(self, event, data):
        async def ack(response):
            print(f"Acknowledgment received for event '{event}':", response)
        await self.sio.emit(event, data)

    async def disconnect(self):
        await self.sio.disconnect()
    
    async def on(self, event_name, handler):
        self.sio.on(event_name, handler)
        
    async def is_connected(self):
        return self.sio.connected
        
    async def send_action(self, action_type, payload=None):
        data = {"action": action_type, "payload": payload or {}}
        await self.send_message("action", data)
        
    async def wait(self):
        await self.sio.wait()
        
    async def join_game(self, username, role):
        data = {
            "username": username,
            "role": role}
        await self.send_message("join_game", data)
        
    async def start_game(self):
        await self.send_message("start_game", {})

    async def end_game(self):
        await self.send_message("end_game", {})

    