import pygame
import sys

pygame.font.init()

class WaitingInLobby:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font_title = pygame.font.SysFont('Roboto', 40)
        self.font_player = pygame.font.SysFont('Roboto', 30)
        self.numero_lobby = -1
        self.player_waiting = []
        self.backgroundImg = pygame.image.load('assets/backgrounds/bg_lobby.png')
    
    def init_attente(self, numero_lobby, *joueurs):
        self.player_waiting = list(joueurs)
        self.player_waiting.append('Vous')
        self.numero_lobby = numero_lobby
    
    def draw(self):
        self.screen.blit(self.backgroundImg, (0, 0))
        
        self.screen.blit(self.font_title.render(f'Lobby {self.numero_lobby}', False, (255, )*3), (50, 50))
        for i in range(len(self.player_waiting)):
            self.screen.blit(self.font_player.render(self.player_waiting[i], False, (255, )*3), (50, 120+i*35))
    
    def update(self, new_player):
        self.player_waiting.append(new_player)