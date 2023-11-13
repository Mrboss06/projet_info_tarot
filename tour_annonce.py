from joueur import *

#dinguerie on fait un tour pour choisir qui fait les annonces

def tour_annonce ():
    prises = []
    joueur_de_prise=[]

    for i in range(4):
        prise=input("prise?")
        joueur=input("joueur?")
        prises.append(prise)
        joueur_de_prise.append(joueur)
        if prise==4:
            break
    prise=max(prises)
    index_preneur=prises.index(prise)
    for i in joueurs:
        i.prises=0                      #index du défenseur=0, index du preneur=index de la prise
    index_preneur.prises=prise
    



