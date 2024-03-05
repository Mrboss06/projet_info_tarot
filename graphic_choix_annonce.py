import pygame
import sys
from graphic_constant import CARD_SIZE, MID_X, MID_Y, SPACE_BETWEEN, CARD_Y, SELECTED_CARD_Y, FONT_20, FONT_25

class ChoixAnnonce:
    def __init__(self, screen: pygame.Surface, cards: dict) -> None:
        self.screen = screen
        self.backgroundImg = pygame.image.load("assets/backgrounds/bg_partie.png")
        self.cardsImg = cards
        self.cards_correspondance = {"coeur": "C", "pique": "P", "carreau": "K", "trefle": "T", "atout": "A"}
        self.selected = -1
        
        self.phase_annonce = True
        self.choisir_annonce_bool = False
        self.annonces_possibles = []
        self.selected_annonce = ""
        self.lst_annonce = []
        self.annonces = []
        
        self.preneur = ""
        self.preneur_annonce = ""
    
    def draw_cards(self, main: 'list[tuple[str, int, int]]'):
        x = round(MID_X-((SPACE_BETWEEN*(len(main)-1))/2)-CARD_SIZE.x/2)
        for i in range(len(main)):
            card: pygame.Surface = self.cardsImg[f"{self.cards_correspondance[main[i][0]]}{main[i][1]}"]
            self.screen.blit(card, 
                            (x+i*SPACE_BETWEEN, CARD_Y-SELECTED_CARD_Y*(self.selected == i)))
    
    def init_annonce(self, annonces_possibles, lst_annonce):
        self.choisir_annonce_bool = True
        self.annonces_possibles = annonces_possibles
        self.lst_annonce = lst_annonce
    
    def choisir_annonce(self, mouse_clicked: bool, mouse_pos: 'tuple[int, int]'):
        height, width = len(self.annonces_possibles)*34 + (len(self.annonces_possibles)+1)*5, 200
        x, y = MID_X - width // 2, MID_Y - height // 2
        bg_rect = pygame.Rect(x, y, width, height)
        
        rect_annonces = [pygame.Rect(x+5, y+5+39*i, width-10, 34) for i in range(len(self.annonces_possibles))]
        pygame.draw.rect(self.screen, "#ffffff", bg_rect, border_radius=5)
        for i in range(len(rect_annonces)):
            if rect_annonces[i].collidepoint(mouse_pos):
                if mouse_clicked:
                    self.selected_annonce = self.annonces_possibles[i]
                color = (0, 255, 255)
            else:
                color = (255,0, 0)
            pygame.draw.rect(self.screen, color, rect_annonces[i], border_radius=5)
            font_surface = FONT_25.render(self.annonces_possibles[i], False, (0, 0, 0))
            self.screen.blit(font_surface, (MID_X-font_surface.get_size()[0]//2, y+7+39*i))
    
    def dessiner_annonce(self):
        for i in range(len(self.annonces)):
            txt = FONT_25.render(f"{self.annonces[i][0]} {('fait une ' + ['petite', 'garde', 'garde-sans', 'garde-contre'][self.annonces[i][1]-1] if self.annonces[i][1] != 0 else 'passe')}", False, (255, 255, 255))
            self.screen.blit(txt, (20, 20+35*i))
    
    def update(self, events, mouse_pos: 'tuple[int, int]', main: 'list[tuple[str, int, int]]'):
        
        self.screen.blit(self.backgroundImg, (0, 0))
        
        mouse_clicked = False
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
                
        if self.choisir_annonce_bool:
            self.choisir_annonce(mouse_clicked, mouse_pos)
            if self.selected_annonce != "":
                self.lst_annonce[0] = self.selected_annonce
                self.choisir_annonce_bool = False
        self.dessiner_annonce()
        
        self.draw_cards(main)