import pygame
import sys # necessaire pour pygame.font.Sysfont

pygame.font.init()

FONT_TITLE = pygame.font.SysFont('Roboto', 40)
FONT_LOBBY_TITLE = pygame.font.SysFont('Roboto', 30)
FONT_LOBBY_MEMBERS = pygame.font.SysFont('Roboto', 20)



class TabSelectLobby:
    
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.lst_lobby_choisi = []
        self.rects = []

    def init_lobby(self, lobbies: "list[tuple[int, tuple[str]]]", lst_lobby_choisi: list) -> None:
        self.lst_lobby_choisi = lst_lobby_choisi
        self.rects.clear()
        for i in range(len(lobbies)):
            self.rects.append(LobbyRect(self.screen, lobbies[i][0], lobbies[i][1], ((i%3)*250+150, (i//3)*210+150)))

    def selectionner_lobby(self, event, mouse_pos: "tuple[int, int]") -> None:
        self.screen.blit(FONT_TITLE.render("Selection De Lobby", False, (255,)*3), (150,50))
        clicked = False
        for ev in event:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
        for rect in self.rects:
            rect.draw(mouse_pos)
            if clicked and rect.rect.collidepoint(*mouse_pos):
                self.lst_lobby_choisi[0]=rect.nb




class LobbyRect:
    
    def __init__(self, screen:pygame.Surface, nb: int, members: "tuple[str]", coord: "tuple[int]") -> None:
        self.screen = screen
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
        pygame.draw.rect(self.screen, color, self.rect, border_radius=20)
        self.screen.blit(FONT_LOBBY_TITLE.render(f"Lobby {self.nb}", False, (0, 0, 0)), (self.coord[0]+10, self.coord[1]+10))
        for i in range(len(self.members)):
            self.screen.blit(FONT_LOBBY_MEMBERS.render(self.members[i], False, (255,255,255)), (self.coord[0]+10, self.coord[1]+50+i*25))