import socket
import threading
import pickle

import game
import tarot_class

HEADER = 64
PORT = 5050
SERVER = '192.168.0.44'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

messages = []
connections = []

lobbies = []


def handle_client(conn: socket.socket, addr, username):
    print(f"[NEW CONNECTION] {username} connected")
    
    dans_un_lobby = False
    
    lst_lobbies = get_liste_lobby()
    msg_send = pickle.dumps(('SERVER', 'action', 'choisir_lobby', lst_lobbies))
    conn.send(msg_send)
    
    connected = True
    while connected:
        msg = pickle.loads(conn.recv(2048))
        
        if msg == DISCONNECT_MESSAGE:
            connected = False
            print(f"[{username}] disconnected")
            conn.send(pickle.dumps(DISCONNECT_MESSAGE))
            messages.append(('[DECONNECTION]', username))
        else:
            if msg[0] == 'SERVER':
                if msg[1] == "action":
                    if msg[2] == "choisir_lobby":
                        if msg[3] == len(lobbies):
                            nouveau_lobby()
                        lobbies[msg[3]][0].nouveaux_joueurs.append((conn, addr, username))
            
    
    connections.remove([conn, addr, username])
    conn.close()


def get_liste_lobby():
    """
    Renvoie la liste de tous les lobbies sous la forme d'une liste
    [
        'Lobby 0(3): joueur 1/joueur 2/joueur 3/'
        'Lobby 1(1): joueur 1/'
        'Lobby 2(0):'
    ]
    
    """
    lst_lobbies = []
    for lob in lobbies:
        current_lobby = ""
        current_lobby += f"Lobby {lob[0].numero_lobby}({len(lob[0].joueurs)}): "
        for joueur in lob[0].joueurs:
            current_lobby += joueur[2]+'/'
        lst_lobbies.append(current_lobby)
    return lst_lobbies
    


def nouveau_lobby():
    partie_tarot = tarot_class.PartieTarot(len(lobbies)+1)
    partie_tarot_thread = threading.Thread(target=partie_tarot.run)
    lobbies.append((partie_tarot, partie_tarot_thread))
    partie_tarot_thread.start()


def start():
    server.listen()
    print(f"[LISTENING] server is listening on {ADDR}")
    nouveau_lobby()
    while True:
        conn, addr = server.accept()
        username = pickle.loads(conn.recv(2048))
        connections.append((conn, addr, username))
        thread = threading.Thread(target=handle_client, args=(conn, addr, username))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {len(connections)}")


print('[STARTING] server is starting...')
start()






