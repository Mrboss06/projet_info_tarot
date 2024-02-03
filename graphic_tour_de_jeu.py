import pygame
import sys
from graphic_constant import CARD_SIZE, MID_X, MID_Y, SPACE_BETWEEN, CARD_Y, SELECTED_CARD_Y, SCREEN_WIDTH, SCREEN_HEIGHT, MID_Y2, SPACE_BETWEEN2
from time import monotonic

FONT_ANNONCE = pygame.font.SysFont('Roboto', 25)
FONT_PSEUDO = pygame.font.SysFont('Roboto', 20)


class Animation:
    
    def __init__(self, screen: pygame.Surface, carte: 'list[str, int, int]', carteImg: pygame.Surface, x_debut: int, y_debut: int, x_final: int, y_final: int, duree_animation: float, list_to_append: list = None) -> None:
        self.screen = screen
        self.carte = carte
        self.carteImg = carteImg
        self.coord_debut = pygame.Vector2(x_debut, y_debut)
        self.coord_fin = pygame.Vector2(x_final, y_final)
        self.duree = duree_animation
        self.coord_a_parcourir = self.coord_fin - self.coord_debut
        self.list_to_append = list_to_append
        self.debut = monotonic()
    
    def draw(self):
        percentage = (monotonic() - self.debut)/self.duree
        if percentage >= 1:
            self.screen.blit(self.carteImg, self.coord_fin)
            if self.list_to_append != None:
                self.list_to_append.append(self.carte)
            return True
        else:
            self.screen.blit(self.carteImg, self.coord_debut + self.coord_a_parcourir * percentage)
            return False


class TourDeJeu:
    def __init__(self, screen: pygame.Surface, cards: dict) -> None:
        self.screen = screen
        self.font = pygame.font.SysFont("Roboto", 20)
        self.cardsImg = cards
        self.cards_correspondance = {"coeur": "C", "pique": "P", "carreau": "K", "trefle": "T", "atout": "A"}
        self.selected = -1
        self.carte_en_jeu = []
        self.animations: 'list[Animation]' = []
        self.joueurs = []
        self.nb_carte_autre_joueur = [18, 18, 18]
        self.jouer_une_carte = False
        self.couleur = 'atout'
        self.carte_jouee = []
        self.cartes_a_jouer_possibles = []
    
    def draw_cards(self, main: 'list[tuple[str, int, int]]'):
        x = round(MID_X-((SPACE_BETWEEN*(len(main)-1))/2)-CARD_SIZE.x/2)
        for i in range(len(main)):
            card: pygame.Surface = self.cardsImg[f"{self.cards_correspondance[main[i][0]]}{main[i][1]}"]
            if self.jouer_une_carte and not main[i] in self.cartes_a_jouer_possibles:
                card = card.copy()
                card.fill((150, 150, 150, 255), None, pygame.BLEND_RGBA_MULT)
            self.screen.blit(card, 
                            (x+i*SPACE_BETWEEN, CARD_Y-SELECTED_CARD_Y*(self.selected == i)))
    
    def draw_pseudos(self):
        txt1 = FONT_PSEUDO.render(self.joueurs[1], False, (255, 255, 255))
        self.screen.blit(txt1, (10, MID_Y - txt1.get_size()[1] // 2))
        
        txt2 = FONT_PSEUDO.render(self.joueurs[2], False, (255, 255, 255))
        self.screen.blit(txt2, (MID_X - txt2.get_size()[0] // 2, 10))
        
        txt3 = FONT_PSEUDO.render(self.joueurs[3], False, (255, 255, 255))
        self.screen.blit(txt3, (SCREEN_WIDTH - txt3.get_size()[0] - 10, MID_Y - txt3.get_size()[1] // 2))
    
    def draw_cartes_autre_joueurs(self):
        carte_dos = self.cardsImg["dos"]
        carte_dos_tournee = pygame.transform.rotate(carte_dos, 90)
        for i in range(self.nb_carte_autre_joueur[0]):
            y = MID_Y2 - ((self.nb_carte_autre_joueur[0] - 1)*SPACE_BETWEEN2 + CARD_SIZE.y ) // 2
            self.screen.blit(carte_dos_tournee, (-220, y + i*SPACE_BETWEEN2))
        
        for i in range(self.nb_carte_autre_joueur[1]):
            x = MID_X - (SPACE_BETWEEN2*(self.nb_carte_autre_joueur[1] - 1) + CARD_SIZE.x) // 2
            self.screen.blit(carte_dos, (x + i*SPACE_BETWEEN2, -220))
        
        for i in range(self.nb_carte_autre_joueur[0]):
            y = MID_Y2 - ((self.nb_carte_autre_joueur[0] - 1)*SPACE_BETWEEN2 + CARD_SIZE.y ) // 2
            self.screen.blit(carte_dos_tournee, (SCREEN_WIDTH - 30, y + i*SPACE_BETWEEN2))
    
    def draw_plis(self):
        for i in range(len(self.carte_en_jeu)):
            carteImg = self.cardsImg[self.cards_correspondance[self.carte_en_jeu[i][0]]+str(self.carte_en_jeu[i][1])]
            self.screen.blit(carteImg, (MID_X - (CARD_SIZE.x + SPACE_BETWEEN*3) // 2 + SPACE_BETWEEN*i, MID_Y2 - CARD_SIZE.y // 2))
            
    
    def carte_jouee_par(self, username: str, carte_en_jeu):
        carte_jouee = carte_en_jeu[-1][0]
        if username == self.joueurs[1]:
            x_debut = - CARD_SIZE.x
            y_debut = MID_Y2 - CARD_SIZE.y // 2
            self.nb_carte_autre_joueur[0] -= 1
        elif username == self.joueurs[2]:
            x_debut = MID_X - CARD_SIZE.x // 2
            y_debut = - CARD_SIZE.y
            self.nb_carte_autre_joueur[1] -= 1
        elif username == self.joueurs[3]:
            x_debut = SCREEN_WIDTH + CARD_SIZE.x
            y_debut = MID_Y2 - CARD_SIZE.y // 2
            self.nb_carte_autre_joueur[2] -= 1
        else:
            x_debut = MID_X - CARD_SIZE.x // 2
            y_debut = CARD_Y
        x_fin = MID_X - (CARD_SIZE.x + SPACE_BETWEEN*3) // 2 + SPACE_BETWEEN*len(self.carte_en_jeu)
        y_fin = MID_Y2 - CARD_SIZE.y // 2
            
        self.animations.append(Animation(self.screen, carte_jouee, self.cardsImg[self.cards_correspondance[carte_jouee[0]] + str(carte_jouee[1])], x_debut, y_debut, x_fin, y_fin, 0.5, self.carte_en_jeu))
    
    def init_cartes_a_jouer_possibles(self, main, couleur: str):
        self.cartes_a_jouer_possibles = set()
        # d'abord on check si le jeu a des cartes de la couleur demandee
        if couleur != 0:
            if couleur != 'atout':
                for i in main:
                    if i[0] == couleur:
                        self.cartes_a_jouer_possibles.add(i)
            # si il y pas la couleur demandee dans le jeu, on check si il y a des atouts
            if self.cartes_a_jouer_possibles == set():
                max_atout = 0
                atouts = set()
                for carte in self.carte_en_jeu:
                    if carte[0] == 'atout' and carte[1] > max_atout:
                        max_atout = carte[1]
                for carte in main:
                    if carte[0] == 'atout' and carte[1] > 0:
                        atouts.add(carte)
                        if max_atout < carte[1]:
                            self.cartes_a_jouer_possibles.add(carte)
                # si il y a pas d'atouts au dessus du plus grand atout joué, alors on ajoute tous les atouts de la main
                if self.cartes_a_jouer_possibles == set():
                    self.cartes_a_jouer_possibles = atouts
        # si il y a pas d'atout dans le jeu, alors on peut jouer ce qu'on veut
        if self.cartes_a_jouer_possibles == set():
            self.cartes_a_jouer_possibles = set(main)
        # et on rajoute l'excuse dans les cartes possibles
        elif ('atout', 0, 4.5) in main:
            self.cartes_a_jouer_possibles.add(('atout', 0, 4.5))
        
    
    def update(self, events, mouse_pos: 'tuple[int, int]', main: 'list[tuple[str, int, int]]'):
        
        mouse_clicked = False
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
        
        x = round(MID_X-((SPACE_BETWEEN*(len(main)-1))/2)-CARD_SIZE.x/2)
        card_rects = [pygame.Rect((x+i*SPACE_BETWEEN, CARD_Y), CARD_SIZE) for i in range(len(main))]
        old_selected = self.selected
        for i in range(len(main)):
            if mouse_clicked and card_rects[i].collidepoint(mouse_pos):
                if old_selected == i:
                    self.selected = -2
                else:
                    self.selected = i
        if self.selected == -2:
            if self.jouer_une_carte and main[old_selected] in self.cartes_a_jouer_possibles:
                self.carte_jouee[1] = old_selected
                self.carte_jouee[2] = main.copy()
                self.carte_jouee[0] = main[old_selected]
                main.pop(old_selected)
            else:
                self.selected = -1
        
        self.draw_cards(main)
        self.draw_pseudos()
        self.draw_cartes_autre_joueurs()
        self.draw_plis()

        for animation in self.animations:
            a = animation.draw()
            if a:
                self.animations.remove(animation)
                del animation
