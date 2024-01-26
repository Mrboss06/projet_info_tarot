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
        self.cards_correspondance = {"coeur": "C", "pique": "P", "carreau": "K", "trefle": "T", "atout": "A"}
        self.selected = -1
    
    def draw_cards(self, main: 'list[tuple[str, int, int]]'):
        x = round(MID_X-((SPACE_BETWEEN*(len(main)-1))/2)-CARD_SIZE.x/2)
        for i in range(len(main)):
            card: pygame.Surface = self.cardsImg[f"{self.cards_correspondance[main[i][0]]}{main[i][1]}"]
            self.screen.blit(card, 
                            (x+i*SPACE_BETWEEN, CARD_Y-SELECTED_CARD_Y*(self.selected == i)))
    
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
                    self.selected = -1
                else:
                    self.selected = i
        
        self.draw_cards(main)