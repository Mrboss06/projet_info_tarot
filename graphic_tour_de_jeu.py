import pygame
import sys
from math import cos, sin, radians
from graphic_constant import CARD_SIZE, MID_X, MID_Y, SPACE_BETWEEN, CARD_Y, SELECTED_CARD_Y

FONT_ANNONCE = pygame.font.SysFont('Roboto', 25)

class TourDeJeu:
    def __init__(self, screen: pygame.Surface, cards: dict) -> None:
        self.screen = screen
        self.font = pygame.font.SysFont("Roboto", 20)
        self.cardsImg = cards
        self.cards_correspondance = {"coeur": "C", "pique": "P", "carreau": "K", "trèfle": "T", "atout": "A"}
        self.selected = -1
        
        self.phase_annonce = True
        self.choisir_annonce_bool = False
        self.annonces_possibles = []
        self.selected_annonce = ""
        self.lst_annonce = []
    
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
            font_surface = FONT_ANNONCE.render(self.annonces_possibles[i], False, (0, 0, 0))
            self.screen.blit(font_surface, (MID_X-font_surface.get_size()[0]//2, y+7+39*i))
    
    def update(self, events, mouse_pos: 'tuple[int, int]', main: 'list[tuple[str, int, int]]'):
        
        mouse_clicked = False
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
        
        if self.choisir_annonce_bool:
            self.choisir_annonce(mouse_clicked, mouse_pos)
            if self.selected_annonce != "":
                self.lst_annonce[0] = self.selected_annonce
                self.choisir_annonce_bool = False
                
        
        x = round(MID_X-((SPACE_BETWEEN*(len(main)-1))/2)-CARD_SIZE.x/2)
        card_rects = [pygame.Rect((x+i*SPACE_BETWEEN, CARD_Y), CARD_SIZE) for i in range(len(main))]
        old_selected = self.selected
        for i in range(len(main)):
            if mouse_clicked and card_rects[i].collidepoint(mouse_pos):
                if old_selected == i:
                    self.selected = -1
                else:
                    self.selected = i
        
        self.draw_cards(main)