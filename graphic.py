import pygame
import sys
import graphic_choisir_lobby

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

graphic_choisir_lobby.init(screen)
#graphic_choisir_lobby.init_lobby([(1, ("J1", "J2", "J3", "J7")), (2, ("J4", "J5")), (4, ("J6",)), (5, tuple())], [-1])

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
        
        graphic_choisir_lobby.selectionner_lobby(ev, mouse_pos)
        
        
        pygame.display.update()

    pygame.quit()