import pygame
import sys
import graphic_choisir_lobby
import graphic_choisir_pseudo

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800


font = pygame.font.SysFont('Roboto', 50)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

graphic_choisir_pseudo.init(screen)
graphic_choisir_lobby.init(screen)
#graphic_choisir_lobby.init_lobby([(1, ("J1", "J2", "J3", "J7")), (2, ("J4", "J5")), (4, ("J6",)), (5, tuple())], [-1])

menu = ''

def run():
    running = True
    while running:
        
        screen.fill((0,0,0))
        
        ev = pygame.event.get()
        
        for event in ev:
            if event.type == pygame.QUIT:
                running = False
        
        mouse_pos = pygame.mouse.get_pos()
        
        #rect_with_mouse(pygame.Rect.collidepoint(rect, *mouse_pos))
        #pygame.draw.rect(screen, (255,0,0), rect)
        
        if menu == 'username':
            screen.blit(font.render("Ton pseudo", False, (255,255,255)), (50, 100))
            graphic_choisir_pseudo.choisir_pseudo(ev)
        elif menu == 'choisir_lobby':
            graphic_choisir_lobby.selectionner_lobby(ev, mouse_pos)
        elif menu == 'attente_dans_lobby':
            screen.blit(font.render("En attente de joueurs", False, (255,)*3), (100, 100))
        else:
            screen.blit(font.render("En attente", False, (255, 255, 255)), (60, 60))
        
        
        pygame.display.update()

    pygame.quit()