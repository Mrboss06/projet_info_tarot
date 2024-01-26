import socket
import threading
import pickle

import joueur
import graphic

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '127.0.0.0'
ADDR = (SERVER, PORT)




client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

main_joueur = joueur.Joueur()

window = graphic.Window(main_joueur)

gui_thread = threading.Thread(target=window.run)

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
    correspondance_carte = {"coeur": 400, "pique": 300, "carreau": 200, "trefle": 100, "atout": 0}
    main.sort(key=lambda x: correspondance_carte[x[0]]+x[1])
    main_joueur.main=main
    window.menu = 'choix_annonce'
    print(f"\nVoici ton jeu:\n{main}\n\n****\n")

def verifier_reception_jeu():
    if main_joueur.main == []:
        send(("LOBBY", "action", "jeu_pas_recu"))

def prise_par_qqn(username, prise):
    window.tab_choix_annonce.annonces.append((username, prise))

def choisir_prise(prises):
    possibilites = ["Petite", "Garde", "Garde-sans", "Garde-contre"]
    plus_petite_annonce_possible = max(prises)+1 if prises != [] else 1
    
    prises_possibles = ["Je passe"] + [possibilites[i+plus_petite_annonce_possible-1] for i in range(0, 5-plus_petite_annonce_possible)]
    lst_annonce = [""]
    window.tab_choix_annonce.init_annonce(prises_possibles, lst_annonce)
    
    while lst_annonce[0] == "": pass
    
    prise = ["Je passe", "Petite", "Garde", "Garde-sans", "Garde-contre"].index(lst_annonce[0])
    
    send(('LOBBY', 'action', 'recevoir_prise', prise))

def faire_son_chien(chien):
    chien_carte_index = []
    window.tab_choix_chien.init(main_joueur.main, chien, chien_carte_index)
    window.menu = 'faire_son_chien'
    
    while chien_carte_index == []: pass
    
    chien_choisi = [main_joueur.main[index] for index in chien_carte_index]
    
    for carte in chien_choisi:
        main_joueur.main.remove(carte)
    
    correspondance_carte = {"coeur": 400, "pique": 300, "carreau": 200, "trefle": 100, "atout": 0}
    main_joueur.main.sort(key=lambda x: correspondance_carte[x[0]]+x[1])
    
    send(('LOBBY', 'action', 'jeux', chien_choisi))

def carte_jouee(username, carte_en_jeu):
    pass

def prise_jouee(username, prise):
    window.tab_attente_chien.init_attente(username, prise)
    window.menu = 'attente_chien'

def debut_partie(username):
    window.menu = 'tour_de_jeu'
    

def jouer_une_carte(cartes_en_jeu, indice_joueur, couleur, tour):
    print(f"c'est à vous de jouer, voici votre jeu: {main_joueur.main}")
    print(f"voici les cartes qui ont déjà été jouées: {cartes_en_jeu}")
    print("indice de la carte à jouer?")
    carte_jouée=int(input())
    while carte_jouée>=len(main_joueur.main):
        print('index trop élevé, réessayez')
        carte_jouée=int(input())
    if main_joueur.main[carte_jouée]==['atout', 0, 4.5] and main_joueur.main!=[['atout', 0, 4.5]]:
        cartes_en_jeu.append([['NULL', 0, 0.5], indice_joueur])
    elif main_joueur==['atout', 0, 4.5]:
        cartes_en_jeu.append(['NULL', 0, 4.5], indice_joueur)
    else:
        cartes_en_jeu.append([main_joueur.main[carte_jouée], indice_joueur])
        if indice_joueur==0 and main_joueur.main[carte_jouée][0]!='NULL': 
            couleur=main_joueur.main[carte_jouée][0]
        if indice_joueur==1 and cartes_en_jeu[0][0][0]=='NULL':
            couleur=main_joueur.main[carte_jouée][0]
    main_joueur.main.pop(carte_jouée)    
    send(('LOBBY', 'action', 'tour_de_jeu_classique', indice_joueur, cartes_en_jeu, couleur, tour))


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

