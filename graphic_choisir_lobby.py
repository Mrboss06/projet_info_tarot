import pygame
import sys # necessaire pour pygame.font.Sysfont

pygame.font.init()


screen = None

font_title = pygame.font.SysFont('Roboto', 40)
font_lobby_title = pygame.font.SysFont('Roboto', 30)
font_lobby_members = pygame.font.SysFont('Roboto', 20)

lst_lobby_choisi = []

rects = []

def init(_screen: pygame.Surface):
    global screen
    screen = _screen

def init_lobby(lobbies: "list[tuple[int, tuple[str]]]", _lst_lobby_choisi: list) -> None:
    global lst_lobby_choisi
    lst_lobby_choisi = _lst_lobby_choisi
    rects.clear()
    for i in range(len(lobbies)):
        rects.append(LobbyRect(lobbies[i][0], lobbies[i][1], ((i%3)*250+150, (i//3)*210+150)))

def selectionner_lobby(event, mouse_pos: "tuple[int, int]") -> None:
    screen.fill((0,0,0))
    screen.blit(font_title.render("Selection De Lobby", False, (255,)*3), (150,50))
    clicked = False
    for ev in event:
        if ev.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
    for rect in rects:
        rect.draw(mouse_pos)
        if clicked and rect.rect.collidepoint(*mouse_pos):
            lst_lobby_choisi[0]=rect.nb




class LobbyRect:
    def __init__(self, nb: int, members: "tuple[str]", coord: "tuple[int]") -> None:
        self.nb = nb
        self.members = members
        self.coord = coord
        self.boxSize = (200, 160)
        self.rect = pygame.Rect(*self.coord,*self.boxSize)
    
    def draw(self, mouse_pos) -> None:
        if self.rect.collidepoint(*mouse_pos):
            color = (0, 255, 255)
        else:
            color = (255, 0, 0)
        pygame.draw.rect(screen, color, self.rect, border_radius=20)
        screen.blit(font_lobby_title.render(f"Lobby {self.nb}", False, (0, 0, 0)), (self.coord[0]+10, self.coord[1]+10))
        for i in range(len(self.members)):
            screen.blit(font_lobby_members.render(self.members[i], False, (255,255,255)), (self.coord[0]+10, self.coord[1]+50+i*25))