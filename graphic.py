import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

rect = pygame.Rect(300,250,50,50)

def rect_with_mouse(value):
    if value:
        rect.x = 280
        rect.y = 230
        rect.size = (90,90)
    else:
        rect.x = 300
        rect.y = 250
        rect.size = (50,50)


running = True
while running:
    
    screen.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    mouse_pos = pygame.mouse.get_pos()
    
    rect_with_mouse(pygame.Rect.collidepoint(rect, *mouse_pos))
    pygame.draw.rect(screen, (255,0,0), rect)
    
    
    
    pygame.display.update()

pygame.quit()