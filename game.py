from random import randint
from joueur import *
import distribution as d


nbPlayer = 4
annonces = ('Petite', 'Garde', 'Garde-sans', 'Garde-contre')
premier_joueur = randint(0, nbPlayer)
chien = []

mains = [Joueur(), Joueur(), Joueur(), Joueur(), Chien()]
joueurs = mains[:4]

def distribuer():
    d.distribuer(mains)