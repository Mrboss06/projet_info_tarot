import pygame
from graphic_constant import FONT_TITLE, FONT_40

COLOR_INACTIVE = pygame.Color('gray')
COLOR_ACTIVE = pygame.Color('black')

pygame.font.init()

class InputBox:

    def __init__(self, screen: pygame.Surface, x: int, y: int, w: int, h: int, text: str = ''):
        self.screen = screen
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT_40.render(text, True, self.color)
        self.active = False
        self.var = []
        self.COLOR_TEXTBOX_INACTIVE = pygame.Color('gray')
        self.COLOR_TEXTBOX_ACTIVE = pygame.Color('black')
        self.COLOR_TEXTBOX = pygame.Color('white')

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = self.COLOR_TEXTBOX_ACTIVE if self.active else self.COLOR_TEXTBOX_INACTIVE
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        if self.text.isidentifier():
                            self.var.append(self.text)
                            self.text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                    # Re-render the text.
                    self.txt_surface = FONT_40.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self):
        # Blit the rect.
        pygame.draw.rect(self.screen, self.COLOR_TEXTBOX, self.rect, border_radius=5)
        pygame.draw.rect(self.screen, self.color, self.rect, 3, border_radius=5)
        # Blit the text.
        self.screen.blit(self.txt_surface, (self.rect.x+10, self.rect.y+10))


class TabChooseUsername:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.backgroundImg = pygame.image.load('assets/backgrounds/bg_main.png')
        self.textinput = InputBox(screen, 100, 400, 220, 60)
        self.boutonJouer = pygame.Rect(100, 500, 200, 60)

    def init_choix_pseudo(self, choix):
        self.textinput.var = choix

    def choisir_pseudo(self, event):
        self.textinput.handle_event(event)
        self.textinput.update()
        self.textinput.draw()
    
    def update(self, events, mouse_clicked, mouse_pos):
        
        self.screen.blit(self.backgroundImg, (0, 0))
        
        #self.screen.blit(FONT_TITLE.render("Tarot", False, (255,255,255)), (100, 100))
        self.choisir_pseudo(events)
        
        if self.boutonJouer.collidepoint(mouse_pos):
            if mouse_clicked and self.textinput.text.isidentifier():
                self.textinput.var.append(self.textinput.text)
                self.textinput.text = ''
            color = (230, 0, 0)
        else:
            color = (255, 0, 0)
        
        pygame.draw.rect(self.screen, color, self.boutonJouer, border_radius=10)
        txt_jouer = FONT_40.render('JOUER', False, 'white')
        self.screen.blit(txt_jouer, (135, 508))