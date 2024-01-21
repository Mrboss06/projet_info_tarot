import socket
import threading
import pickle

import joueur

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '192.168.0.46'
ADDR = (SERVER, PORT)



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
    print("\nVoici les parties que tu peux rejoindre:\n")
    possible_lobbies = []
    for lobby in lst_lobbies:
        if lobby[0].count('/')<4:
            print(lobby[0])
            possible_lobbies.append(str(lobby[1]))
    print(f"Tape + pour creer un nouveau lobby, sinon le numero du lobby que tu veux rejoindre")
    lobby = input()
    while lobby != '+' and not lobby in possible_lobbies:
        print("\nTon choix n'est pas dans les possibilitees")
        print(f"Tape + pour creer un nouveau lobby, sinon le numero du lobby que tu veux rejoindre")
        lobby = input()
    print()
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
    print(f"[LOBBY] le joueur {pseudo} a rejoint la partie !")

def username_est_valide(username):
    for charactere in username:
        if not (charactere.isalnum() or charactere in '-_'):
            return False
    return True


print("Bienvenue au jeu de tarot!\n\n")
print("Quel est votre pseudonyme ?")
username = input()

while not username_est_valide(username):
    username = input("\nLe pseudonyme donné n'est pas valide\n\nPseudonyme: ")


client.connect(ADDR)
send(username)

server_thread = threading.Thread(target=handle_server)

server_thread.start()

