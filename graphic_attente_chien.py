import pygame
import sys
from graphic_constant import MID_X

FONT_TEXT = pygame.font.SysFont('Roboto', 40)

class AttenteChien:
    
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
    
    
    def init_attente(self, pseudo, prise):
        self.preneur = pseudo
        self.prise = prise
    
    def update(self):
        
        txt = FONT_TEXT.render(f"{self.preneur} fait une {['petite', 'garde', 'garde-sans', 'garde-contre'][self.prise-1]}", False, (255, 255, 255))
        self.screen.blit(txt, (MID_X-txt.get_size()[0]//2, 100))
        
        txt2 = FONT_TEXT.render("Ce joueur fait son chien", False, (255, 255, 255))
        self.screen.blit(txt2, (MID_X - txt2.get_size()[0]//2, 150))