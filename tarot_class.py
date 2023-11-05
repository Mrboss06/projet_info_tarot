import socket
import threading
import pickle

import joueur


class PartieTarot:
    
    def __init__(self, numero_lobby) -> None:
        self.joueurs = []
        # dans nouveaux joueurs, on rajoute les nouveaux participants, de la forme (socket.socket, addresse, username)
        self.nouveaux_joueurs = []
        self.numero_lobby = numero_lobby
        self.a_commence = False
    
    
    def run(self):
        while len(self.joueurs) != 4:
            if self.nouveaux_joueurs != []:
                for nv_joueur in self.nouveaux_joueurs:
                    self.send_msg_to_all(f'Le joueur {nv_joueur[2]} rejoint la partie')
                    self.joueurs.append(nv_joueur + (joueur.Joueur(),))
                    self.send_msg(nv_joueur[0], f"Tu as rejoint le lobby {self.numero_lobby}")
                self.nouveaux_joueurs.clear()
        self.send_msg_to_all('Tous les joueurs sont connectes, la partie commence')
        self.a_commence = True
        while 1: pass
    
    def send_msg_to_all(self, msg):
        for connection in self.joueurs:
            msg_send = pickle.dumps(('LOBBY', self.numero_lobby, msg))
            connection[0].send(msg_send)
    
    def send_msg(self, conn, msg):
        msg_send = pickle.dumps(('LOBBY', self.numero_lobby, msg))
        conn.send(msg_send)