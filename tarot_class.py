import socket
import threading
import pickle
import time
import random

import joueur


class PartieTarot:
    
    def __init__(self, numero_lobby) -> None:
        # un joueur c'est (socket.socket, addr, username, joueur.Joueur)
        self.joueurs = []
        # dans nouveaux joueurs, on rajoute les nouveaux participants, de la forme (socket.socket, addresse, username)
        self.nouveaux_joueurs = []
        self.numero_lobby = numero_lobby
        self.a_commence = False
        self.prises = []
    
    def run(self):
        while len(self.joueurs) != 4:
            if self.nouveaux_joueurs != []:
                for nv_joueur in self.nouveaux_joueurs:
                    self.send_msg_to_all("message", f'Le joueur {nv_joueur[2]} rejoint la partie')
                    self.joueurs.append(nv_joueur + (joueur.Joueur(),))
                    self.send_msg(nv_joueur[0], "message", f"Tu as rejoint le lobby {self.numero_lobby}")
                self.nouveaux_joueurs.clear()
        self.send_msg_to_all("message", 'Tous les joueurs sont connectes, la partie commence')
        self.a_commence = True
        self.distribuer()
        self.faire_le_choix_des_prises()
        self.lancer_la_partie()
        while 1: pass
    
    def send_msg_to_all(self, type, *msg):
        for connection in self.joueurs:
            msg_send = pickle.dumps(('LOBBY', type, *msg))
            connection[0].send(msg_send)
        time.sleep(0.1)
    
    def send_msg(self, conn, type, *msg):
        msg_send = pickle.dumps(('LOBBY', type, *msg))
        conn.send(msg_send)
        time.sleep(0.1)
        

    def distribuer(self):
        jeu=[['coeur', 1, 0.5], ['coeur', 2, 0.5], ['coeur', 3, 0.5], ['coeur', 4, 0.5], ['coeur', 5, 0.5], ['coeur', 6, 0.5], ['coeur', 7, 0.5], ['coeur', 8, 0.5], ['coeur', 9, 0.5], ['coeur', 10, 0.5], ['coeur', 11, 1.5], ['coeur', 12, 2.5], ['coeur', 13, 3.5], ['coeur', 14, 4.5], ['pique', 1, 0.5], ['pique', 2, 0.5], ['pique', 3, 0.5], ['pique', 4, 0.5], ['pique', 5, 0.5], ['pique', 6, 0.5], ['pique', 7, 0.5], ['pique', 8, 0.5], ['pique', 9, 0.5], ['pique', 10, 0.5], ['pique', 11, 1.5], ['pique', 12, 2.5], ['pique', 13, 3.5], ['pique', 14, 4.5], ['carreau', 1, 0.5], ['carreau', 2, 0.5], ['carreau', 3, 0.5], ['carreau', 4, 0.5], ['carreau', 5, 0.5], ['carreau', 6, 0.5], ['carreau', 7, 0.5], ['carreau', 8, 0.5], ['carreau', 9, 0.5], ['carreau', 10, 0.5], ['carreau', 11, 1.5], ['carreau', 12, 2.5], ['carreau', 13, 3.5], ['carreau', 14, 4.5], ['trefle', 1, 0.5], ['trefle', 2, 0.5], ['trefle', 3, 0.5], ['trefle', 4, 0.5], ['trefle', 5, 0.5], ['trefle', 6, 0.5], ['trefle', 7, 0.5], ['trefle', 8, 0.5], ['trefle', 9, 0.5], ['trefle', 10, 0.5], ['trefle', 11, 1.5], ['trefle', 12, 2.5], ['trefle', 13, 3.5], ['trefle', 14, 4.5], ['atout', 1, 4.5], ['atout', 2, 0.5], ['atout', 3, 0.5], ['atout', 4, 0.5], ['atout', 5, 0.5], ['atout', 6, 0.5], ['atout', 7, 0.5], ['atout', 8, 0.5], ['atout', 9, 0.5], ['atout', 10, 0.5], ['atout', 11, 0.5], ['atout', 12, 0.5], ['atout', 13, 0.5], ['atout', 14, 0.5], ['atout', 15, 0.5], ['atout', 16, 0.5], ['atout', 17, 0.5], ['atout', 18, 0.5], ['atout', 19, 0.5], ['atout', 20, 0.5], ['atout', 21, 4.5], ['atout', 0, 4.5]]
        a=0
        for i in range (4):
            self.joueurs[i][3].main=[]
        for j in range (4):
            for k in range(18):
                d=random.randint(0,77-k-a)
                self.joueurs[j][3].main.append(jeu[d])
                jeu.pop(d)
            a+=18    
        self.chien=jeu
        for i in range(4):
            print(self.joueurs[i][3].main)
        for i in range(4):
            self.send_msg(self.joueurs[i][0], 'action', 'recevoir_jeu', self.joueurs[i][3].main)
        #self.send_msg_to_all("action", "verifier_reception_jeu")

    def faire_le_choix_des_prises(self):
        nb_prise_actuel = 0
        for i in range(4):
            self.send_msg(self.joueurs[i][0], 'action', 'choisir_prise', self.prises)
            while len(self.prises) == nb_prise_actuel:
                pass
            nb_prise_actuel = len(self.prises)
        self.send_msg_to_all("message", f'les prises sont {self.prises}')
    
    def recevoir_prise(self, username, prise):
        self.send_msg_to_all("message", f"{username} {'fait une '+('petite', 'garde', 'garde-sans', 'garde-contre')[prise-1] if prise != 0 else 'passe'}!")
        self.prises.append(prise)
    
    def jeu_pas_recu(self, username):
        for joueur in self.joueurs:
            if joueur[2] == username:
                self.send_msg(joueur[0], "action", "recevoir_jeu", joueur[3].main)

    def faire_son_chien(self, username_preneur):
        for i in range(4):
            if self.joueurs[i][2]==username_preneur:
                self.joueurs[i][3].main.append(self.chien)
                for j in range(6):
                    a=input("Enlever une carte (index de la carte à enlever): ")
                    self.joueurs[i][3].plis.append(self.joueurs[i][3][a])
                    self.joueurs[i][3].main.pop(a)
                self.send_msg(joueur[i][0], "action", "recevoir_jeu", joueur[i][3].main)

    def lancer_la_partie(self):
        self.send_msg(self.joueurs[0][0], "action", "jouer_une_carte", [], 0, "")


    def tour_de_jeu_classique(self, username , indice_joueur, carte_jouée, cartes_en_jeu, couleur):
        self.joueurs[indice_joueur][3].main.pop(carte_jouée)
        atouts_en_jeu=[]
        if len(cartes_en_jeu)==1:
            couleur=cartes_en_jeu[0][0][0]
        if len(cartes_en_jeu)!=4:
            self.send_msg(self.joueurs[indice_joueur+1][0], "action", "jouer_une_carte", cartes_en_jeu, indice_joueur+1, couleur)
        elif len(cartes_en_jeu)==4:
            for j in range(4):
                if cartes_en_jeu[j][0][0]=="atout" and cartes_en_jeu[j][0][1]!=0:
                    atouts_en_jeu.append([cartes_en_jeu[j][0], cartes_en_jeu[j][1]])
            if atouts_en_jeu!=[]:
                plus_gros_atout=0
                for j in range(len(atouts_en_jeu)):
                    if atouts_en_jeu[j][0][1]>plus_gros_atout:
                        plus_gros_atout=atouts_en_jeu[j][0][1]
                        c=j
                gagnant=atouts_en_jeu[c][1]
                c=0
                plus_gros_atout=0
                atouts_en_jeu=[]
            else:
                plus_grosse_carte=0
                c=0
                for j in range(4):
                    if cartes_en_jeu[j][0][0]==couleur and cartes_en_jeu[j][0][1]>plus_grosse_carte:
                        c=j        
                        plus_grosse_carte=cartes_en_jeu[j][0][1]
                gagnant=cartes_en_jeu[c][1]
                plus_grosse_carte=0
                c=0      
            self.joueurs[gagnant][3].plis.append(cartes_en_jeu)
            cartes_en_jeu=[]
            for joueur in range(4):
                if joueur!=gagnant: 
                    self.joueurs.append(self.joueurs.pop(0))
                else: 
                    break    
            for i in range(4):
                print(self.joueurs[i][3].plis)
            self.send_msg(self.joueurs[0][0], "action", "jouer_une_carte", [], 0, couleur)
            
    
            #vérifier quelle carte gagne (comparer à la carte du 1er joueur)
            #trouver quelles cartes sont légales