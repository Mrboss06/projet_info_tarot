import pygame
from graphic_constant import MID_X, SPACE_BETWEEN, CARD_SIZE, CARD_Y, SELECTED_CARD_Y, SCREEN_HEIGHT

FONT_TITLE = pygame.font.SysFont('Roboto', 40)

class FaireChien:
    
    def __init__(self, screen: pygame.Surface, cardsImg) -> None:
        self.screen = screen
        self.cardsImg = cardsImg
        self.cards_correspondance = {"coeur": "C", "pique": "P", "carreau": "K", "trefle": "T", "atout": "A"}
        self.selected = -1
    
    def init(self, main: list, chien: list):
        self.main = main
        self.main.extend(chien)
        self.chien = []
    
    def draw_cards(self, main: 'list[tuple[str, int, int]]'):
        x = round(MID_X-((SPACE_BETWEEN*(len(main)-1))/2)-CARD_SIZE.x/2)
        rects = []
        if x < 0:
            sublist1 = main[:18]
            sublist2 = main[18:]
            x1 = round(MID_X-((SPACE_BETWEEN*(len(sublist1)-1))/2)-CARD_SIZE.x/2)
            x2 = round(MID_X-((SPACE_BETWEEN*(len(sublist2)-1))/2)-CARD_SIZE.x/2)
            for i in range(len(sublist1)):
                card: pygame.Surface = self.cardsImg[f"{self.cards_correspondance[sublist1[i][0]]}{sublist1[i][1]}"]
                rects.append(pygame.Rect(x1+i*SPACE_BETWEEN, SCREEN_HEIGHT-10-CARD_SIZE.y-SELECTED_CARD_Y*(self.selected == i), CARD_SIZE.x, CARD_SIZE.y))
                self.screen.blit(card, 
                                (x1+i*SPACE_BETWEEN, SCREEN_HEIGHT-10-CARD_SIZE.y-SELECTED_CARD_Y*(self.selected == i)))
            for i in range(len(sublist2)):
                card: pygame.Surface = self.cardsImg[f"{self.cards_correspondance[sublist2[i][0]]}{sublist2[i][1]}"]
                rects.append(pygame.Rect(x2+i*SPACE_BETWEEN, SCREEN_HEIGHT-10-SELECTED_CARD_Y-CARD_SIZE.y*2-SELECTED_CARD_Y*(self.selected == i+18), CARD_SIZE.x, CARD_SIZE.y))
                self.screen.blit(card, 
                                (x2+i*SPACE_BETWEEN, SCREEN_HEIGHT-10-SELECTED_CARD_Y-CARD_SIZE.y*2-SELECTED_CARD_Y*(self.selected == i+18)))
        else:
            for i in range(len(main)):
                card: pygame.Surface = self.cardsImg[f"{self.cards_correspondance[main[i][0]]}{main[i][1]}"]
                rects.append(pygame.Rect((x+i*SPACE_BETWEEN, CARD_Y), CARD_SIZE))
                self.screen.blit(card, 
                                (x+i*SPACE_BETWEEN, CARD_Y-SELECTED_CARD_Y*(self.selected == i)))
        return rects
    
    def update(self, events, mouse_pos: 'tuple[int, int]'):
        
        mouse_clicked = False
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
        
        card_rects = self.draw_cards(self.main)
        
        old_selected = self.selected
        for i in range(len(self.main)):
            if mouse_clicked and card_rects[i].collidepoint(mouse_pos):
                if old_selected == i:
                    self.selected = -1
                else:
                    self.selected = i
        
        self.screen.blit(FONT_TITLE.render('Fait ton chien', False, (255,255,255)), (20, 20))
        