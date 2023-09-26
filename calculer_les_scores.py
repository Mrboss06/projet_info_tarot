joueurs =["1", "2", "3", "4"]
annonces = ["petite", "garde", 'garde-sans', 'garde-contre']
scores=[0,0,0,0]

parties = []
score = []

SCORES_BOUTS=[56,51,41,36]
MULTIPLICATEURS=[1,2,4,6]
ANNONCES_ANNEXES=[10,10]

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

def ajouter_annonces_annexes(annonces_annexes, index_suite, joueur_annonces_annexes, vainqueur_derniere_levee,score_du_preneur,index_annonce):
    if annonces_annexes[0]==1:
        if score_du_preneur>=0:
            score[index_du_preneur]+=10*(index_suite+1)*4
            score[0],score[1],score[2],score[3]-=10*(index_suite+1)
        else:
            score[index_du_preneur]-=10*(index_suite+1)*4
            score[0],score[1],score[2],score[3]+=10*(index_suite+1)  
        annonces_annexes.pop(0)    
    elif annonces_annexes[0]==2:
       if vainqueur_derniere_levee==index_du_preneur:
          score[index_du_preneur]+=10*(index_annonce+1)*4
          score[0],score[1],score[2],score[3]-=10*(index_annonce+1)    
       else:
          score[index_du_preneur]-=10*(index_annonce+1)*4
          score[0],score[1],score[2],score[3]+=10*(index_annonce+1)    
            


        

    

    
        


    



