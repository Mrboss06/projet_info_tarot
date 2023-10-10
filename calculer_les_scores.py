joueurs =["1", "2", "3", "4"]
annonces = ["petite", "garde", 'garde-sans', 'garde-contre']
score=[0,0,0,0]

parties = []
scores = []

SCORES_BOUTS=[56,51,41,36]
MULTIPLICATEURS=[1,2,4,6]
ANNONCES_ANNEXES=[10,10]
SCORES_SUITES=[20,30,40]

index_du_preneur=input()
index_prise=input()
nb_bouts=input()
score_donne=input()
annonces_annexes=input()
résultats_de_la_donne=[index_du_preneur, index_prise, nb_bouts, score_donne, annonces_annexes]
scores.append(index_prise, nb_bouts, score_donne, index_du_preneur)
parties.append(index_du_preneur, index_prise, nb_bouts, score_donne)



def calculer_les_scores(indice_partie, nb_bouts, index_prise):
    scoring=scores[indice_partie].split()                                    #séparer les scores. ATTENTION!: différencier Scores: liste où l'on stocke les infos utiles à l'issue d'une partie et score liste contenant les 4 scores
    score_du_preneur=scoring[2]-SCORES_BOUTS[nb_bouts]
    if score_du_preneur>=0:
        score_preneur=(score_du_preneur+25)*MULTIPLICATEURS[index_prise]*3
    else:
        score_preneur=(score_du_preneur-25)*MULTIPLICATEURS[index_prise]*3  
    score_adversaires=-score_preneur/3
    score[index_du_preneur]+=score_preneur-score_adversaires
    score[0],score[1],score[2],score[3]+=score_adversaires,score_adversaires,score_adversaires,score_adversaires

def ajouter_annonces_annexes(annonces_annexes, index_suite, vainqueur_derniere_levee,score_du_preneur,index_prise,):
    for i in range(5):
       if annonces_annexes!=[]:
          if annonces_annexes[0]==1:                                               #suites: +-4*score de l'index de suite pour le preneur, puis +-10*score de l'index de la suite pour tous
              if score_du_preneur>=0:                                             
                 score[index_du_preneur]+=SCORES_SUITES[index_suite]*4
                 score[0],score[1],score[2],score[3]-=SCORES_SUITES[index_suite]
              else:
                   score[index_du_preneur]-=SCORES_SUITES[index_suite]*4
                   score[0],score[1],score[2],score[3]+=SCORES_SUITES[index_suite]
              annonces_annexes.pop(0)  
          elif annonces_annexes[0]==2:                                            #petit au bout: +-4*10*index de la prise pour le preneur puis +-10*index de la suite pour tout le monde
                if vainqueur_derniere_levee==index_du_preneur:
                  score[index_du_preneur]+=10*(index_prise+1)*4
                  score[0],score[1],score[2],score[3]-=10*(index_prise+1)    
                else:
                 score[index_du_preneur]-=10*(index_prise+1)*4
                 score[0],score[1],score[2],score[3]+=10*(index_prise+1) 
                annonces_annexes.pop(0)     

        

    

    
        


    



