import socket
import threading
import pickle

import joueur

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '192.168.0.44'
ADDR = (SERVER, PORT)



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
            if msg[0] == 'SERVER':
                if msg[1] == 'message':
                    print(msg[2])
                elif msg[1] == 'action':
                    threading.Thread(target=eval(msg[2]), args=msg[3:]).start()
            if msg[0] == 'LOBBY':
                print(f"[LOBBY{msg[1]}] {msg[2]}")
        else:
            print(msg)


def choisir_lobby(lst_lobbies):
    for lobby in lst_lobbies:
        print(lobby)
    print(f"({len(lst_lobbies)+1}) pour un nouveau lobby")
    lobby = input('Quel lobby ? ')
    while int(lobby)<1 or int(lobby)>len(lst_lobbies)+1:
        lobby = input("Vous avez rentré un mauvais lobby\nQuel lobby choisissez vous ?")
    client.send(pickle.dumps(("SERVER", "action", "choisir_lobby", int(lobby))))

def username_est_valide(username):
    for charactere in username:
        if not (charactere.isalnum() or charactere in '-_'):
            return False
    return True

username = input('Pseudonyme: ')

while not username_est_valide(username):
    username = input("\nLe pseudonyme donné n'est pas valide\n\nPseudonyme: ")


client.connect(ADDR)
send(username)

server_thread = threading.Thread(target=handle_server)

server_thread.start()

