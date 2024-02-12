import socket
import threading
import pickle

import joueur

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

SERVER = '127.0.0.0'
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

def joueur_quitte_lobby(pseudo):
    print(f"Le joueur {pseudo} quitte le lobby")

def dans_lobby(numero, pseudos):
    print(f'tu rentres dans le lobby {numero} avec les joueurs: {pseudos}')


def recevoir_jeu(main):
    main_joueur.main=main
    print(f"\nVoici ton jeu:\n{main}\n\n****\n")


def verifier_reception_jeu():
    if main_joueur.main == []:
        send(("LOBBY", "action", "jeu_pas_recu"))

def prise_par_qqn(username, prise):
    print(f"{username} a fait une '{['Passe', 'Petite', 'Garde', 'Garde-sans', 'Garde-contre'][prise]}'")

def faire_son_chien(chien):
    chien_joueur=[]
    a='-1'
    for i in range(6):
        main_joueur.main.append(chien[i])
    jeu=main_joueur.main    
    for i in range(6):
        print(f"Voici votre main: {jeu}")
        print("Choisissez l'index d'une carte à retirer:")
        carte_a_retirer=int(input())
        while carte_a_retirer>=len(jeu):
            print('Index trop élevé, réessayez.')
            carte_a_retirer=int(input())
        chien_joueur.append(main_joueur.main[carte_a_retirer])
        jeu.pop(carte_a_retirer)
    while a!='1' and a!='0':
        print(f'Voici votre chien: {chien_joueur}')    
        print('Si il vous convient, appuyez sur 1, sinon pour le refaire,appuyez sur 0:')
        a=input()
        if a!='0' and a!='1':
            print('ce caractère n est pas valide')    
    if a=='1':
        send(('LOBBY', 'action', 'jeux', chien_joueur))
    elif a=='0':
        faire_son_chien(chien_joueur)   

def prise_jouee(username, prise):
    print(f"C'est {username} qui prend, avec une {['Petite', 'garde', 'garde-sans', 'garde-contre'][prise-1]}")

def debut_partie(username):
    print(f"La partie commence, le joueur {username} joue")

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

def carte_jouee(username, carte_en_jeu):
    print(f"{username} a joue une carte, voici les cartes en jeu: '{carte_en_jeu}'")

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

def fin_du_pli():
    print('fin du pli')

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
