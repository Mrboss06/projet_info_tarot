import pygame
from graphic_constant import MID_X, SPACE_BETWEEN, CARD_SIZE, CARD_Y, SELECTED_CARD_Y, SCREEN_HEIGHT

FONT_TITLE = pygame.font.SysFont('Roboto', 40)
FONT_BUTTON = pygame.font.SysFont('Roboto', 30)

class FaireChien:
    
    def __init__(self, screen: pygame.Surface, cardsImg) -> None:
        self.screen = screen
        self.backgroundImg = pygame.image.load("assets/backgrounds/bg_partie.png")
        self.cardsImg = cardsImg
        self.cards_correspondance = {"coeur": "C", "pique": "P", "carreau": "K", "trefle": "T", "atout": "A"}
        self.selected = []
    
    def init(self, main: list, chien: list, chien_carte_index: list):
        self.main = main
        self.main.extend(chien)
        self.chien = []
        self.chien_carte_index = chien_carte_index
        nb_carte_non_atout = 0
        for carte in self.main:
            if carte[0] != 'atout' and carte[1] != 14:
                nb_carte_non_atout += 1
        if nb_carte_non_atout < 6:
            self.atout_autorise = True
        else:
            self.atout_autorise = False
    
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
                if i in self.selected:
                    card = card.copy()
                    card.fill((255, 255, 0, 255), None, pygame.BLEND_RGBA_MULT)
                rects.append(pygame.Rect(x1+i*SPACE_BETWEEN, SCREEN_HEIGHT-10-CARD_SIZE.y, CARD_SIZE.x, CARD_SIZE.y))
                self.screen.blit(card, 
                                (x1+i*SPACE_BETWEEN, SCREEN_HEIGHT-10-CARD_SIZE.y))
            for i in range(len(sublist2)):
                card: pygame.Surface = self.cardsImg[f"{self.cards_correspondance[sublist2[i][0]]}{sublist2[i][1]}"]
                if i+18 in self.selected:
                    card = card.copy()
                    card.fill((255, 255, 0, 255), None, pygame.BLEND_RGBA_MULT)
                rects.append(pygame.Rect(x2+i*SPACE_BETWEEN, SCREEN_HEIGHT-10-SELECTED_CARD_Y-CARD_SIZE.y*2, CARD_SIZE.x, CARD_SIZE.y))
                self.screen.blit(card, 
                                (x2+i*SPACE_BETWEEN, SCREEN_HEIGHT-10-SELECTED_CARD_Y-CARD_SIZE.y*2))
        return rects
    
    def update(self, events, mouse_pos: 'tuple[int, int]'):
        
        self.screen.blit(self.backgroundImg, (0, 0))
        
        mouse_clicked = False
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
        
        card_rects = self.draw_cards(self.main)
        
        selected_card = -1
        for i in range(len(self.main)):
            if mouse_clicked and card_rects[i].collidepoint(mouse_pos):
                selected_card = i
        if selected_card in self.selected:
            self.selected.remove(selected_card)
        elif self.selected != -1:
            if ((self.main[selected_card][0] == 'atout' and self.atout_autorise and not self.main[selected_card] in {0, 1, 21}) or (self.main[selected_card][0] != 'atout' and self.main[selected_card][1] != 14)) and len(self.selected) < 6:
                self.selected.append(selected_card)
        
        if len(self.selected) == 6:
            button_rect = pygame.Rect(MID_X-100, 100, 200, 40)
            if button_rect.collidepoint(mouse_pos):
                color = (0, 255, 255)
            else:
                color = (255, 0, 0)
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(MID_X-105, 95, 210, 50), border_radius=5)
            pygame.draw.rect(self.screen, color, button_rect, border_radius=5)
            txt = FONT_BUTTON.render('Soumettre', False, (255, 255, 255))
            self.screen.blit(txt, (MID_X-txt.get_size()[0]//2, 105))
            if mouse_clicked and button_rect.collidepoint(mouse_pos):
                self.chien_carte_index.extend(self.selected)
        
        self.screen.blit(FONT_TITLE.render('Fait ton chien', False, (255,255,255)), (20, 20))