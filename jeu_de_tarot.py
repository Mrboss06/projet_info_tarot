from random import *

coeur = [ ('coeur', 1), ('coeur', 2), ('coeur', 3),('coeur', 4),('coeur', 5),('coeur', 6),('coeur', 7),('coeur', 8),('coeur', 9), ('coeur', 10), ('coeur', 11), ('coeur', 12), ('coeur', 13), ('coeur', 14)]
pique= [ ('pique', 1), ('pique', 2), ('pique', 3), ('pique', 4), ('pique', 5), ('pique', 6), ('pique', 7), ('pique', 8), ('pique', 9), ('pique', 10), ('pique', 11), ('pique', 12), ('pique', 13), ('pique', 14)]
carreau= [ ('carreau', 1), ('carreau', 2), ('carreau', 3), ('carreau', 4), ('carreau', 5), ('carreau', 6), ('carreau', 7), ('carreau', 8), ('carreau', 9), ('carreau', 10), ('carreau', 11), ('carreau', 12), ('carreau', 13), ('carreau', 14)]
trèfle= [ ('trèfle', 1), ('trèfle', 2), ('trèfle', 3), ('trèfle', 4), ('trèfle', 5), ('trèfle', 6), ('trèfle', 7), ('trèfle', 8), ('trèfle', 9), ('trèfle', 10), ('trèfle', 11), ('trèfle', 12), ('trèfle', 13), ('trèfle', 14)]
jeu=[ ('coeur', 1), ('coeur', 2), ('coeur', 3),('coeur', 4),('coeur', 5),('coeur', 6),('coeur', 7),('coeur', 8),('coeur', 9), ('coeur', 10), ('coeur', 11), ('coeur', 12), ('coeur', 13), ('coeur', 14), ('pique', 1), ('pique', 2), ('pique', 3), ('pique', 4), ('pique', 5), ('pique', 6), ('pique', 7), ('pique', 8), ('pique', 9), ('pique', 10), ('pique', 11), ('pique', 12), ('pique', 13), ('pique', 14), ('carreau', 1), ('carreau', 2), ('carreau', 3), ('carreau', 4), ('carreau', 5), ('carreau', 6), ('carreau', 7), ('carreau', 8), ('carreau', 9), ('carreau', 10), ('carreau', 11), ('carreau', 12), ('carreau', 13), ('carreau', 14), ('trèfle', 1), ('trèfle', 2), ('trèfle', 3), ('trèfle', 4), ('trèfle', 5), ('trèfle', 6), ('trèfle', 7), ('trèfle', 8), ('trèfle', 9), ('trèfle', 10), ('trèfle', 11), ('trèfle', 12), ('trèfle', 13), ('trèfle', 14), ('none',1),('none',2),('none',3),('none',4),('none',5),('none',6),('none',7),('none',8),('none',9),('none',10),('none',11),('none',12),('none',13),('none',14),('none',15),('none',16),('none',17),('none',18),('none',19),('none',20),('none',21),('none',0)]
atouts= [('none',1),('none',2),('none',3),('none',4),('none',5),('none',6),('none',7),('none',8),('none',9),('none',10),('none',11),('none',12),('none',13),('none',14),('none',15),('none',16),('none',17),('none',18),('none',19),('none',20),('none',21),('none',0)]
#excuse à la fin des atouts sous le nombre 0
ORDRE_DES_COULEURS_DANS_LE_JEU=['coeur', 'pique', 'carreau', 'trèfle']
 
#distribution
chien=[]
def distribuer(joueurs,chien):
    joueurss=joueurs.split()
    for i in range (4):
        joueurss[i].main=[]
    for i in range (78):
        joueurss[randint(0,5)].main.append(jeu[i])    



