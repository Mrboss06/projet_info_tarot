joueurs =["1", "2", "3", "4"]
annonces = ["petite", "garde", 'garde-sans', 'garde-contre']

parties = []
score = []

SCORES_BOUTS=[56,51,41,36]
MULTIPLICATEURS=[1,2,4,6]

def recuperer_les_resultats_de_la_donne(index_du_preneur, index_annonce, nb_bouts, score_donne):
    parties.append((index_du_preneur, index_annonce, nb_bouts, score_donne))
    score.append(index_annonce, nb_bouts, score_donne, index_du_preneur)




def calculer_les_scores(indice_partie, nb_bouts, index_annonce):
    scoring=score[indice_partie].split()
    score_du_preneur=scoring[2]-SCORES_BOUTS[nb_bouts]
    if score_du_preneur>=0:
        score_preneur=(score_du_preneur+25)*MULTIPLICATEURS[index_annonce]
    else:
        score_preneur=(score_du_preneur-25)*MULTIPLICATEURS[index_annonce]    


