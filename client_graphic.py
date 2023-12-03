import socket
import threading
import pickle

import joueur
import graphic

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '192.168.0.18'
ADDR = (SERVER, PORT)


window = graphic.Window()

gui_thread = threading.Thread(target=window.run)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

main_joueur = joueur.Joueur()

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
                    threading.Thread(target=eval(msg[2]), args=(msg[3:] if len(msg)>3 else [])).start()
            if msg[0] == 'LOBBY':
                if msg[1] == "action":
                    threading.Thread(target=eval(msg[2]), args=(msg[3:] if len(msg)>3 else [])).start()
                elif msg[1] == "message":
                    print(f"[LOBBY] {msg[2]}")
        else:
            print(msg)


def choisir_lobby(lst_lobbies):
    possible_lobbies = []
    for lobby in lst_lobbies:
        if lobby[0].count('/')<4:
            possible_lobbies.append(lobby)
    choix = [-1]
    possible_lobbies = [(lobby[1], [member for member in lobby[0][lobby[0].index(":")+2:].split("/")[:-1]]) for lobby in lst_lobbies]
    print(possible_lobbies)
    window.tab_select_lobby.init_lobby(possible_lobbies, choix)
    window.menu = 'choisir_lobby'
    while choix[0]==-1: pass
    lobby = choix[0]
    for lob in possible_lobbies:
        if lob[0] == lobby:
            window.tab_waiting_in_lobby.init_attente(lobby, *lob[1])
    window.menu = 'attente_dans_lobby'
    if lobby != '+':
        lobby = int(lobby)
    client.send(pickle.dumps(("SERVER", "action", "choisir_lobby", lobby)))



def recevoir_jeu(main):
    main_joueur.main=main
    print(f"\nVoici ton jeu:\n{main}\n\n****\n")


def verifier_reception_jeu():
    if main_joueur.main == []:
        send(("LOBBY", "action", "jeu_pas_recu"))


def choisir_prise(prises):
    print("\n** C'est à vous d'annoncer **\nQue voulez vous faire ?\n\ntaper:\n1 pour passer")
    possibilites = ["pour une petite", "pour une garde", "pour une garde-sans", "pour une garde-contre"]
    plus_petite_annonce_possible = max(prises)+1 if prises != [] else 1
    for i in range(0, 5-plus_petite_annonce_possible):
        print(f"{i+2} {possibilites[i+plus_petite_annonce_possible-1]}")
    prise = int(input())
    if prise != 1:
        prise += plus_petite_annonce_possible - 2
    else:
        prise -= 1
    send(('LOBBY', 'action', 'recevoir_prise', prise))

def nouveau_joueur_dans_lobby(pseudo):
    print(f"[LOBBY] le joueur {pseudo} a rejoint la partie")
    window.tab_waiting_in_lobby.update(pseudo)

def username_est_valide(username):
    for charactere in username:
        if not (charactere.isalnum() or charactere in '-_'):
            return False
    return True


def choisir_pseudo():
    choix = []
    window.tab_choose_username.init_choix_pseudo(choix)
    window.menu = 'username'
    print(window.menu)
    while choix==[]: pass
    window.menu = ''
    print(f"[CLIENT] ton pseudo est {choix[0]}")
    return choix[0]

gui_thread.start()


username = choisir_pseudo()

client.connect(ADDR)
send(username)

server_thread = threading.Thread(target=handle_server)

server_thread.start()

