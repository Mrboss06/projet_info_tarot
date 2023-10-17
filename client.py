import socket
import threading
import pickle

import joueur

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '172.21.6.50'
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

main = joueur.Joueur()

def send(msg):
    message = pickle.dumps(msg)
    client.send(message)


def handle_server():
    while True:
        msg = pickle.loads(client.recv(2048))
        if msg == DISCONNECT_MESSAGE:
            print('[CLIENT] disconnecting...')
            break
        elif type(msg) != str:
            if msg[0] == 'main':
                main.main = msg[1]
                print('ta main est: ', main.main)
        else:
            print(msg)


def loop():
    username = input('your username: ')
    send(username)
    while True:
        message = input()
        if message == 'disconnect':
            send(DISCONNECT_MESSAGE)
            break
        else:
            send(message)


loop_thread = threading.Thread(target=loop)
server_thread = threading.Thread(target=handle_server)

loop_thread.start()
server_thread.start()

