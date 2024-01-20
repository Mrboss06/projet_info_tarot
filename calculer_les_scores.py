import tarot_class
import joueur

points=[0,0,0,0]
#scores=[score dvu preneur, nb_bouts(du preneur)(index), index de la prise, index du preneur,
#        annonces annexes(liste de jusqu'à 2 de longueur avec les annonces annexes(petit au bout, poignée) dans l'ordre suivant: suites puis petit au bout), 
#        index suite , vainqueur de la dernière levée (index du joueur ayant remporté le dernier pli) ]
scores=[56, 2, 1, 0, [1,2], 1, 0]
parties = []

SCORES_BOUTS=[56,51,41,36]
MULTIPLICATEURS=[1,2,4,6]
SCORES_SUITES=[20,30,40]


def calculer_scores(scores, points):             
    score_du_preneur=scores[0]-SCORES_BOUTS[scores[1]]
    if score_du_preneur>=0:
        score_preneur=(score_du_preneur+25)*MULTIPLICATEURS[scores[2]]*3
    else:
        score_preneur=(score_du_preneur-25)*MULTIPLICATEURS[scores[2]]*3  
    score_adversaires=-score_preneur/3
    points[scores[3]]+=score_preneur-score_adversaires
    for i in range (4): points[i]+=score_adversaires
    return score_du_preneur, points

def ajouter_annonces_annexes(scores, score_du_preneur, points):
    for i in range(5):
       if scores[4]!=[]:
          if scores[4][0]==1:                                               #suites: +-4*score de l'index de suite pour le preneur, puis +-1*score de l'index de la suite pour tous
              if score_du_preneur>=0:                                             
                 points[scores[3]]+=SCORES_SUITES[scores[5]]*4
                 for i in range (4): points[i]-=SCORES_SUITES[scores[5]]
              else:
                   points[scores[3]]-=SCORES_SUITES[scores[5]]*4
                   for i in range (4): points[i]+=SCORES_SUITES[scores[5]]
              scores[4].pop(0)  
          elif scores[4][0]==2:                                            #petit au bout: +-4*10*index de la prise pour le preneur puis +-10*index de la suite pour tout le monde
                if scores[6]==scores[3]:
                  points[scores[3]]+=10*(scores[2]+1)*4
                  for i in range (4): points[i]-=10*(scores[2]+1)    
                else:
                 points[scores[3]]-=10*(scores[2]+1)*4
                 for i in range (4): points[i]+=10*(scores[2]+1) 
    return points

calculer_scores(scores, points)
ajouter_annonces_annexes(scores, 0, points)
print(points)  
#creer self.points, ajouter les points à chaque joueur
    
        



    



