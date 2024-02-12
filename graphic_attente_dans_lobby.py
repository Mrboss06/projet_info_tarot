import pygame
import sys
from graphic_constant import FONT_40, FONT_50, MID_X, SCREEN_HEIGHT


pygame.font.init()

class WaitingInLobby:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.numero_lobby = -1
        self.player_waiting = []
        self.backgroundImg = pygame.image.load('assets/backgrounds/bg_lobby.png')
    
    def init_attente(self, numero_lobby: int, quitter_lobby_lst: list, *joueurs) -> None:
        self.player_waiting = list(joueurs)
        self.player_waiting.append('Vous')
        self.numero_lobby = numero_lobby
        self.quitter_lobby_lst = quitter_lobby_lst
    
    def draw(self, mouse_pos, mouse_clicked):
        
        self.screen.blit(self.backgroundImg, (0, 0))
        
        txt = FONT_50.render(f'Lobby {self.numero_lobby}', False, (255, )*3)
        self.screen.blit(txt, (MID_X - txt.get_size()[0] // 2, 50))
        
        for i in range(len(self.player_waiting)):
            txt = FONT_40.render(self.player_waiting[i], False, (255, )*3)
            self.screen.blit(txt, (MID_X - txt.get_size()[0] // 2, 150+i*45))
        
        boutonQuitter = pygame.Rect(MID_X - 100, SCREEN_HEIGHT - 100, 200, 50)
        txt = FONT_40.render('QUITTER', False, 'white')
        
        if boutonQuitter.collidepoint(mouse_pos):
            if mouse_clicked:
                self.quitter_lobby_lst[0] = 1
            color = (218, 0, 0)
        else:
            color = (255, 0, 0)
        
        pygame.draw.rect(self.screen, color, boutonQuitter, border_radius=10)
        self.screen.blit(txt, (MID_X - txt.get_size()[0] // 2, SCREEN_HEIGHT - 98))
    
    def update(self, new_player):
        self.player_waiting.append(new_player)