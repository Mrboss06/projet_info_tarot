import pygame
import sys
import graphic_choisir_lobby
import graphic_choisir_pseudo
import graphic_attente_dans_lobby

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800


class Window:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.SysFont('Roboto', 50)
        self.tab_choose_username = graphic_choisir_pseudo.TabChooseUsername(self.screen)
        self.tab_select_lobby = graphic_choisir_lobby.TabSelectLobby(self.screen)
        self.tab_waiting_in_lobby = graphic_attente_dans_lobby.WaitingInLobby(self.screen)
        self.menu = ''

    def run(self):
        running = True
        while running:
            
            self.screen.fill((0,0,0))
            
            ev = pygame.event.get()
            
            for event in ev:
                if event.type == pygame.QUIT:
                    running = False
            
            mouse_pos = pygame.mouse.get_pos()
            
            #rect_with_mouse(pygame.Rect.collidepoint(rect, *mouse_pos))
            #pygame.draw.rect(screen, (255,0,0), rect)
            
            if self.menu == 'username':
                self.screen.blit(self.font.render("Ton pseudo", False, (255,255,255)), (50, 100))
                self.tab_choose_username.choisir_pseudo(ev)
            elif self.menu == 'choisir_lobby':
                self.tab_select_lobby.selectionner_lobby(ev, mouse_pos)
            elif self.menu == 'attente_dans_lobby':
                self.tab_waiting_in_lobby.draw()
            else:
                self.screen.blit(self.font.render("En attente", False, (255, 255, 255)), (60, 60))
            
            
            pygame.display.update()

        pygame.quit()