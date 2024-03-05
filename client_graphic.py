import socket
import threading
import pickle
import time

import joueur
import graphic

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '172.21.6.50'
ADDR = (SERVER, PORT)




client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_joueur = joueur.Joueur()
window = graphic.Window(main_joueur)
username = ""

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
    timer = time.monotonic()
    while choix[0]==-1:
        if time.monotonic() - timer > 5:
            send(('SERVER', 'action', 'obtenir_lst_lobby'))
            timer = time.monotonic()
        
    lobby = choix[0]
    if lobby != '+':
        lobby = int(lobby)
    client.send(pickle.dumps(("SERVER", "action", "choisir_lobby", lobby)))

def mettre_a_jour_list_lobby(list_lobby: list):
    possible_lobbies = []
    for lobby in list_lobby:
        if lobby[0].count('/')<4:
            possible_lobbies.append(lobby)
    choix = [-1]
    possible_lobbies = [(lobby[1], [member for member in lobby[0][lobby[0].index(":")+2:].split("/")[:-1]]) for lobby in list_lobby]
    window.tab_select_lobby.mettre_a_jour_list_lobby(possible_lobbies)

def dans_lobby(numero_lobby: int, pseudos: 'list[str]'):
    window.menu = 'attente_dans_lobby'
    choix = [-1]
    window.tab_waiting_in_lobby.init_attente(numero_lobby, choix, *pseudos)
    
    while window.menu == 'attente_dans_lobby' and choix[0] == -1: pass
    
    if window.menu == 'attente_dans_lobby':
        send(('SERVER', "action", 'quitter_lobby'))
        
def debut_prises(list_pseudo: 'list[str]'):
    window.tab_tour_de_jeu.joueurs = list_pseudo
    window.tab_tour_de_jeu.joueurs[window.tab_tour_de_jeu.joueurs.index(username)] = "Vous"

def recevoir_jeu(main):
    correspondance_carte = {"coeur": 400, "pique": 300, "carreau": 200, "trefle": 100, "atout": 0}
    main.sort(key=lambda x: correspondance_carte[x[0]]+x[1])
    main_joueur.main=main
    window.menu = 'choix_annonce'
    for _ in range(4):
        if window.tab_tour_de_jeu.joueurs[0] != "Vous":
            window.tab_tour_de_jeu.joueurs.append(window.tab_tour_de_jeu.joueurs.pop(0))

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
    
    send(('LOBBY', 'action', 'recevoir_chien_choisi', chien_choisi))

def carte_jouee(username, carte_en_jeu):
    window.tab_tour_de_jeu.carte_jouee_par(username, carte_en_jeu)

def prise_jouee(username, prise):
    window.tab_attente_chien.init_attente(username, prise)
    window.menu = 'attente_chien'

def debut_partie(username):
    window.menu = 'tour_de_jeu'

def jouer_une_carte(cartes_en_jeu, indice_joueur, couleur, tour):
    print(f"c'est à vous de jouer, voici votre jeu: {main_joueur.main}")
    print(f"voici les cartes qui ont déjà été jouées: {cartes_en_jeu}")
    print("indice de la carte à jouer?")
    
    window.tab_tour_de_jeu.jouer_une_carte = True
    window.tab_tour_de_jeu.init_cartes_a_jouer_possibles(main_joueur.main, couleur)
    
    carte_jouee_lst = [0, 0, 0]
    
    window.tab_tour_de_jeu.carte_jouee = carte_jouee_lst
    while carte_jouee_lst[0] == 0: pass
    window.tab_tour_de_jeu.jouer_une_carte = False
    carte_jouee_index = carte_jouee_lst[1]
    carte_jouee = carte_jouee_lst[0]
    main = carte_jouee_lst[2]
    
    if main[carte_jouee_index]==('atout', 0, 4.5) and main!=[('atout', 0, 4.5)]:
        cartes_en_jeu.append([('NULL', 0, 0.5), indice_joueur])
    elif main==[('atout', 0, 4.5)]:
        cartes_en_jeu.append(('NULL', 0, 4.5), indice_joueur)
    else:
        cartes_en_jeu.append([main[carte_jouee_index], indice_joueur])
        if indice_joueur==0 and main[carte_jouee_index][0]!='NULL': 
            couleur=main[carte_jouee_index][0]
        if indice_joueur==1 and cartes_en_jeu[0][0][0]=='NULL':
            couleur=main[carte_jouee_index][0]
    send(('LOBBY', 'action', 'tour_de_jeu_classique', indice_joueur, cartes_en_jeu, couleur, tour))

def fin_du_pli():
    window.tab_tour_de_jeu.carte_en_jeu.clear()

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

def connect_to_server():
    global username
    username = choisir_pseudo()
    client.connect(ADDR)
    send(username)

    server_thread = threading.Thread(target=handle_server)
    server_thread.start()
    

start_thread = threading.Thread(target=connect_to_server)
start_thread.start()

window.run()





