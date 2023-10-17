import socket
import threading
import pickle

import game

HEADER = 64
PORT = 5050
SERVER = '172.21.6.50'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

messages = []
connections = []


game_is_ready = False


def handle_client(conn: socket.socket, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    
    username = pickle.loads(conn.recv(2048))
    connections[connections.index([conn, addr])].append(username)
    
    connected = True
    while connected:
        msg = pickle.loads(conn.recv(2048))
        
        if msg == DISCONNECT_MESSAGE:
            connected = False
            print(f"[{username}] disconnected")
            conn.send(pickle.dumps(DISCONNECT_MESSAGE))
            messages.append(('[DECONNECTION]', username))
        
        else:
            print(f"{username}: {msg}")
            messages.append((msg, username))
    
    connections.remove([conn, addr, username])
    conn.close()



def handle_messages():
    while True:
        new_messages = messages.copy()
        if new_messages != []:
            for message in new_messages:
                for conn in connections:
                    if message[1] != conn[-1]:
                        conn[0].send(pickle.dumps(f"{message[1]}: {message[0]}"))
                messages.remove(message)


message_thread = threading.Thread(target=handle_messages)



def handle_game():
    while len(connections) != 4: pass
    messages.append(('All players are connected, waiting for them to be ready', '[SERVER]'))
    players_are_ready = False
    while not players_are_ready:
        players_are_ready = True
        for conn in connections:
            if len(conn) == 2:
                players_are_ready = False
    messages.append(('All players are ready, starting the game', '[SERVER]'))
    game.distribuer()
    for i in range(4):
        data = pickle.dumps(('main', game.joueurs[i].main))
        connections[i][0].send(data)
    messages.append(('Les mains sont distribuées', '[SERVER]'))

game_thread = threading.Thread(target=handle_game)



def start():
    server.listen()
    print(f"[LISTENING] server is listening on {ADDR}")
    message_thread.start()
    game_thread.start()
    while True:
        conn, addr = server.accept()
        connections.append([conn, addr])
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {len(connections)}")


print('[STARTING] server is starting...')
start()






