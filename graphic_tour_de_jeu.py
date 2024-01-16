import pygame
import sys






class TourDeJeu:
    def __init__(self, screen, cards) -> None:
        self.screen = screen
        self.font = pygame.font.SysFont("Roboto", 20)
        self.cardsImg = cards
        self.cards_correspondance = {"coeur": "C", "pic": "P", "carreaux": "K", "trèfle": "T", "atout": "A"}
    
    def draw_cards(self, main):
        for i in range(len(main)):
            self.screen.blit(self.cardsImg[f"{self.cards_correspondance[main[i][0]]}{main[i][1]}"], (i*20, 100))
            