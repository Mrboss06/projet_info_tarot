joueurs =["1", "2", "3", "4"]
annonces = ["petite", "garde", 'garde-sans', 'garde-contre']

parties = []
scores = []

def recuperer_les_resultats_de_la_donne(index_du_preneur, index_annonce, nb_bouts, score_donne):
    parties.append((index_du_preneur, index_annonce, nb_bouts, score_donne))


def calculer_les_scores():
    