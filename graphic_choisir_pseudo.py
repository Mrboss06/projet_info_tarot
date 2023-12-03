import pygame

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.SysFont('Roboto', 30)


class InputBox:

    def __init__(self, screen: pygame.Surface, x: int, y: int, w: int, h: int, text: str =''):
        self.screen = screen
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.var = []

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
                self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.var.append(self.text)
                        self.text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                    # Re-render the text.
                    self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self):
        # Blit the rect.
        pygame.draw.rect(self.screen, self.color, self.rect, 3)
        # Blit the text.
        self.screen.blit(self.txt_surface, (self.rect.x+10, self.rect.y+7))


class TabChooseUsername:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.textinput = InputBox(screen, 400, 375, 100, 50)

    def init_choix_pseudo(self, choix):
        self.textinput.var = choix

    def choisir_pseudo(self, event):
        self.textinput.handle_event(event)
        self.textinput.update()
        self.textinput.draw()