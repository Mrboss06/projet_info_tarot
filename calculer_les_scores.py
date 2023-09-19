joueurs =["1", "2", "3", "4"]
annonces = ["petite", "garde", 'garde-sans', 'garde-contre']

parties = []
score = []

def recuperer_les_resultats_de_la_donne(index_du_preneur, index_annonce, nb_bouts, score_donne):
    parties.append((index_du_preneur, index_annonce, nb_bouts, score_donne))
    score.append(index_annonce, nb_bouts, score_donne, index_du_preneur)




def calculer_les_scores(indice_partie, scores):
    scoring=score[indice_partie].split()
    
