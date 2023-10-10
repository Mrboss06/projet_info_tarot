from random import randint
from joueur import Joueur


nbPlayer = 4

premier_joueur = randint(0, nbPlayer)

joueurs = [Joueur() for _ in range(nbPlayer)]