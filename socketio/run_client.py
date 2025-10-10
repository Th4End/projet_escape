from socket_client import SocketClient
import asyncio
import time

SERVEUR_URL = "http://localhost:5000" # Mettre l'URL du serveur
USERNAME = "Louis" # Mettre méthode ou variable pour renseignrer le nom de l'utilisateur
ROLE = "Analyst"# Mettre méthode ou variable pour renseignrer le role de l'utilisateur

def on_user_joined(data):
    print("User joined:", data)
    
def on_user_left(data):
    print("User left:", data)
    
def on_action_response(data):
    print("Action response from server:", data)
    
def on_room_created(data):
    print("Room created:", data)
    
def on_room_joined(data):
    print("Room joined:", data)
    
def on_room_left(data):
    print("Room left:", data)

def on_start_game(data):
    print("Game started:", data)
    
def on_game_update(data):
    print("Game update:", data)
    
def on_end_game(data):
    print("Game ended:", data)
    
def on_puzzle_solved(data):
    print("Puzzle solved:", data)

async def main():
    client = SocketClient(SERVEUR_URL, debug=True)
    
    client.sio.on("user_joined", on_user_joined)
    client.sio.on("user_left", on_user_left)
    client.sio.on("room_created", on_room_created)
    client.sio.on("room_joined", on_room_joined)
    client.sio.on("room_left", on_room_left)
    client.sio.on("action_response", on_action_response)
    client.sio.on("game_update", on_game_update)
    client.sio.on("start_game", on_start_game)
    client.sio.on("end_game", on_end_game)
    client.sio.on("puzzle_solved", on_puzzle_solved)
    
    print("Connecting to server...")
    await client.connect()
    
    if await client.is_connected():
        print("[INFO] Client connected successfully.")

        # Simulation du comportement utilisateur :
        await client.join_game(USERNAME, ROLE)
        await asyncio.sleep(1)

        await client.start_game()
        await asyncio.sleep(1)

        await client.send_action("solve_puzzle", {"puzzle_id": 1})
        await asyncio.sleep(1)

        await client.end_game()

    else:
        print("[ERROR] Failed to connect to server.")
        
    try:
        await client.wait()
    except KeyboardInterrupt:
        print("Disconnecting from server...")
        await client.disconnect()
        print("Disconnected.")

if __name__ == '__main__':  
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass