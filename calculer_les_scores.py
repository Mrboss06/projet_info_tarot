joueurs =["1", "2", "3", "4"]
annonces = ["petite", "garde", 'garde-sans', 'garde-contre']
scores=[0,0,0,0]

parties = []
score = []

SCORES_BOUTS=[56,51,41,36]
MULTIPLICATEURS=[1,2,4,6]
ANNONCES_ANNEXES=[20,30,40,10]

index_du_preneur=input()
index_annonce=input()
nb_bouts=input()
score_donne=input()
annonces_annexes=input()
résultats_de_la_donne=[index_du_preneur, index_annonce, nb_bouts, score_donne, annonces_annexes]
score.append(index_annonce, nb_bouts, score_donne, index_du_preneur)
parties.append(index_du_preneur, index_annonce, nb_bouts, score_donne)



def calculer_les_scores(indice_partie, nb_bouts, index_annonce):
    scoring=score[indice_partie].split()
    score_du_preneur=scoring[2]-SCORES_BOUTS[nb_bouts]
    if score_du_preneur>=0:
        score_preneur=(score_du_preneur+25)*MULTIPLICATEURS[index_annonce]*3
    else:
        score_preneur=(score_du_preneur-25)*MULTIPLICATEURS[index_annonce]*3  
    score_adversaires=-score_preneur/3
    score[index_du_preneur]+=score_preneur-score_adversaires
    score[0],score[1],score[2],score[3]+=score_adversaires,score_adversaires,score_adversaires,score_adversaires

def ajouter_annonces_annexes(annonces_annexes, joueur_annonces_annexes, vainqueur_dernière_levée,score_du_preneur):
    if annonces_annexes==1:
        

    

    
        


    



