import socket
import threading
import pickle

import tarot_class

HEADER = 64
PORT = 5050
SERVER = '192.168.0.46'
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
    
    lobby = None
    
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
                        if msg[3] == '+':
                            print("nouveau lobby")
                            numero = nouveau_lobby()
                        else:
                            numero = msg[3]
                        lobby = numero
                        lobbies[obtenir_lobby_par_numero(numero)][0].nouveaux_joueurs.append((conn, addr, username))
            if msg[0] == 'LOBBY':
                if msg[1] == 'action':
                    threading.Thread(target=eval(f"lobbies[{obtenir_lobby_par_numero(lobby)}][0].{msg[2]}"), args=[username, *msg[3:]]).start()
                
            
    
    connections.remove([conn, addr, username])
    conn.close()

def get_liste_lobby():
    """
    Renvoie la liste de tous les lobbies sous la forme d'une liste
    Par exemple:
    [
        ('Lobby 0(3 personnes): joueur 1/joueur 2/joueur 3/', 0)
        ('Lobby 1(1 personne): joueur 1/', 1)
        ('Lobby 2(0 personne):', 2)
    ]
    
    """
    lst_lobbies = []
    for lob in lobbies:
        current_lobby = ""
        current_lobby += f"Lobby {lob[0].numero_lobby}({len(lob[0].joueurs)} personne{'s' if len(lob[0].joueurs)>1 else ''}): "
        for joueur in lob[0].joueurs:
            current_lobby += joueur[2]+'/'
        lst_lobbies.append((current_lobby, lob[0].numero_lobby))
    return lst_lobbies

def nouveau_lobby():
    """
    Crée un nouveau lobby, soit une nouvelle instance de la classe PartieTarot dans un nouveau Thread
    Le nouveau thread et la nouvelle instance sont ajoutés à la liste 'lobbies' sous la forme d'un tuple (tarot_class.PartieTarot, threading.Thread)
    """
    min_numero_lobby = 1
    while type(obtenir_lobby_par_numero(min_numero_lobby))==int:
        min_numero_lobby += 1
    partie_tarot = tarot_class.PartieTarot(min_numero_lobby)
    partie_tarot_thread = threading.Thread(target=partie_tarot.run)
    lobbies.append((partie_tarot, partie_tarot_thread))
    partie_tarot_thread.start()
    print(f"[NUMBER OF LOBBY] {len(lobbies)}")
    return min_numero_lobby

def obtenir_lobby_par_numero(numero):
    """
    Renvoie un tuple (tarot_class.PartieTarot, threading.Thread) de 'lobbies'
    Le PartieTarot de ce tuple a comme 'numero_lobby' l'argument donné à la fonction
    Renvoie False si aucun lobby n'a ce numero
    """
    for lobby in range(len(lobbies)):
        if lobbies[lobby][0].numero_lobby == numero:
            return lobby
    return False

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






