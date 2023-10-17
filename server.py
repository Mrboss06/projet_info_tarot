import socket
import threading

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


def handle_client(conn: socket.socket, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    
    username = conn.recv(2048).decode(FORMAT)
    connections[connections.index([conn, addr])].append(username)
    
    connected = True
    while connected:
        msg = conn.recv(2048).decode(FORMAT)
        
        if msg == DISCONNECT_MESSAGE:
            connected = False
            print(f"[{username}] disconnected")
            conn.send(DISCONNECT_MESSAGE.encode(FORMAT))
            if username != '':
                messages.append(('[DECONNECTION]', addr, username))
            else:
                messages.append(('[DECONNECTION]', addr))
        
        else:
            print(f"{username}: {msg}")
            if username != '':
                messages.append((msg, addr, username))
            else:
                messages.append((msg, addr))
    
    connections.remove([conn, addr, username])
    conn.close()


def handle_messages():
    while True:
        new_messages = messages.copy()
        if new_messages != []:
            for message in new_messages:
                for conn in connections:
                    if message[1] != conn[1]:
                        username = message[-1]
                        conn[0].send(f"{username}: {message[0]}".encode(FORMAT))
                messages.remove(message)


message_thread = threading.Thread(target=handle_messages)


def start():
    server.listen()
    print(f"[LISTENING] server is listening on {ADDR}")
    message_thread.start()
    while True:
        conn, addr = server.accept()
        connections.append([conn, addr])
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")


print('[STARTING] server is starting...')
start()






