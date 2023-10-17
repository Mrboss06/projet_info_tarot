from random import *
from joueur import *

coeur = [ ('coeur', 1), ('coeur', 2), ('coeur', 3),('coeur', 4),('coeur', 5),('coeur', 6),('coeur', 7),('coeur', 8),('coeur', 9), ('coeur', 10), ('coeur', 11), ('coeur', 12), ('coeur', 13), ('coeur', 14)]
pique= [ ('pique', 1), ('pique', 2), ('pique', 3), ('pique', 4), ('pique', 5), ('pique', 6), ('pique', 7), ('pique', 8), ('pique', 9), ('pique', 10), ('pique', 11), ('pique', 12), ('pique', 13), ('pique', 14)]
carreau= [ ('carreau', 1), ('carreau', 2), ('carreau', 3), ('carreau', 4), ('carreau', 5), ('carreau', 6), ('carreau', 7), ('carreau', 8), ('carreau', 9), ('carreau', 10), ('carreau', 11), ('carreau', 12), ('carreau', 13), ('carreau', 14)]
trèfle= [ ('trèfle', 1), ('trèfle', 2), ('trèfle', 3), ('trèfle', 4), ('trèfle', 5), ('trèfle', 6), ('trèfle', 7), ('trèfle', 8), ('trèfle', 9), ('trèfle', 10), ('trèfle', 11), ('trèfle', 12), ('trèfle', 13), ('trèfle', 14)]
atouts= [('atout',1),('atout',2),('atout',3),('atout',4),('atout',5),('atout',6),('atout',7),('atout',8),('atout',9),('atout',10),('atout',11),('atout',12),('atout',13),('atout',14),('atout',15),('atout',16),('atout',17),('atout',18),('atout',19),('atout',20),('atout',21),('atout',0)]
jeu=[ ('coeur', 1), ('coeur', 2), ('coeur', 3),('coeur', 4),('coeur', 5),('coeur', 6),('coeur', 7),('coeur', 8),('coeur', 9), ('coeur', 10), ('coeur', 11), ('coeur', 12), ('coeur', 13), ('coeur', 14), ('pique', 1), ('pique', 2), ('pique', 3), ('pique', 4), ('pique', 5), ('pique', 6), ('pique', 7), ('pique', 8), ('pique', 9), ('pique', 10), ('pique', 11), ('pique', 12), ('pique', 13), ('pique', 14), ('carreau', 1), ('carreau', 2), ('carreau', 3), ('carreau', 4), ('carreau', 5), ('carreau', 6), ('carreau', 7), ('carreau', 8), ('carreau', 9), ('carreau', 10), ('carreau', 11), ('carreau', 12), ('carreau', 13), ('carreau', 14), ('trèfle', 1), ('trèfle', 2), ('trèfle', 3), ('trèfle', 4), ('trèfle', 5), ('trèfle', 6), ('trèfle', 7), ('trèfle', 8), ('trèfle', 9), ('trèfle', 10), ('trèfle', 11), ('trèfle', 12), ('trèfle', 13), ('trèfle', 14), ('atout',1),('atout',2),('atout',3),('atout',4),('atout',5),('atout',6),('atout',7),('atout',8),('atout',9),('atout',10),('atout',11),('atout',12),('atout',13),('atout',14),('atout',15),('atout',16),('atout',17),('atout',18),('atout',19),('atout',20),('atout',21),('atout',0)]

#excuse à la fin des atouts sous le nombre 0
ORDRE_DES_COULEURS_DANS_LE_JEU=['coeur', 'pique', 'carreau', 'trèfle']


joueurs = [Joueur(),Joueur(),Joueur(),Joueur(),Chien()]


#distribution
chien=[]
def distribuer(joueurs):
    a=0
    for i in range (5):
        joueurs[i].main=[]
    for j in range (4):
        for k in range(18):
            d=randint(0,77-k-a)
            joueurs[j].main.append(jeu[d])
            jeu.pop(d)
        a+=18    
    joueurs[4].main=jeu


distribuer(joueurs)
 
for i in joueurs :
    print(i.main)  
  




