import socket
import threading
import pickle

import joueur

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '192.168.200.111'
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

def faire_son_chien(chien):
    for i in range(6):
        main_joueur.main.append(chien[i])
    for i in range(6):
        print(f"Voici votre main: {main_joueur.main}")
        print("Choisissez l'index d'une carte à retirer:")
        carte_a_retirer=int(input())
        main_joueur.plis.append(main_joueur.main[carte_a_retirer])
        main_joueur.main.pop(carte_a_retirer)
    send(('LOBBY', 'action', 'jeux'))    



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

def username_est_valide(username):
    for charactere in username:
        if not (charactere.isalnum() or charactere in '-_'):
            return False
    return True

def jouer_une_carte(cartes_en_jeu, indice_joueur, couleur):
    print(f"c'est à vous de jouer, voici votre jeu: {main_joueur.main}")
    print(f"voici les cartes qui ont déjà été jouées: {cartes_en_jeu}")
    print("indice de la carte à jouer?")
    carte_jouée=int(input())
    cartes_en_jeu.append([main_joueur.main[carte_jouée], indice_joueur])
    if indice_joueur==0: 
        couleur=main_joueur.main[carte_jouée]
    main_joueur.main.pop(carte_jouée)    
    send(('LOBBY', 'action', 'tour_de_jeu_classique', indice_joueur, carte_jouée, cartes_en_jeu, couleur))

def fin_de_partie(plis, index_preneur, index_prise):
    score=0
    nb_bouts=0
    for pli in plis:
        for i in range(len(pli)):
            score+=pli[i][0][2]
            if pli[i][0]==['atout', 1, 4.5] or pli[i][0]==['atout', 21, 4.5] or pli[i][0]==['atout', 0, 4.5]:
                nb_bouts+=1
    send(('LOBBY', 'action', 'scores', score, nb_bouts, index_prise, index_preneur))
#rajouter les annonces annexes#



    
    


print("Bienvenue au jeu de tarot!\n\n")
print("Quel est votre pseudonyme ?")
username = input()

while not username_est_valide(username):
    username = input("\nLe pseudonyme donné n'est pas valide\n\nPseudonyme: ")


client.connect(ADDR)
send(username)

server_thread = threading.Thread(target=handle_server)

server_thread.start()

