from random import randint
from joueur import Joueur


nbPlayer = 4
annonces = ('Petite', 'Garde', 'Garde-sans', 'Garde-contre')
premier_joueur = randint(0, nbPlayer)
chien = []

joueurs = [Joueur() for _ in range(nbPlayer)]