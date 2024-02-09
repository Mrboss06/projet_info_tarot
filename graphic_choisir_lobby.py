import pygame
import sys # necessaire pour pygame.font.Sysfont

from graphic_constant import FONT_40, FONT_30, FONT_20, MID_X, SENSIBLITE_SOURIS

pygame.font.init()



class TabSelectLobby:
    
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.lst_lobby_choisi = []
        self.rects = []
        self.backgroundImg = pygame.image.load('assets/backgrounds/bg_lobby.png')
        self.y = 0

    def init_lobby(self, lobbies: "list[tuple[int, tuple[str]]]", lst_lobby_choisi: list) -> None:
        self.lst_lobby_choisi = lst_lobby_choisi
        self.rects.clear()
        for i in range(len(lobbies)):
            self.rects.append(RectLobby(self.screen, lobbies[i][0], lobbies[i][1], pygame.Vector2((i%3)*250+150, (i//3)*210+150)))
        self.rects.append(RectNewLobby(self.screen, pygame.Vector2(((i+1)%3)*250+150, ((i+1)//3)*210+150)))

    def selectionner_lobby(self, event, mouse_pos: "tuple[int, int]") -> None:
        
        self.screen.blit(self.backgroundImg, (0, 0))
        txt = FONT_40.render('Selection de Lobby', False, 'white')
        self.screen.blit(txt, (MID_X - txt.get_size()[0] // 2,self.y + 50))
        clicked = False
        for ev in event:
            if ev.type == pygame.MOUSEWHEEL:
                self.y = min(0, max(self.y + ev.y * SENSIBLITE_SOURIS, - (len(self.rects) // 3 + bool(len(self.rects) % 3)) * 210 + 650))
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    clicked = True
        for rect in self.rects:
            rect.draw(mouse_pos, self.y)
            if clicked and rect.rect.collidepoint(*mouse_pos):
                self.lst_lobby_choisi[0]=rect.nb




class RectBase:
    
    def __init__(self, screen: pygame.Surface, coord: pygame.Vector2, color, color_selected) -> None:
        self.screen = screen
        self.coord = coord
        self.color, self.color_selected = color, color_selected
        self.boxSize = pygame.Vector2(200, 160)
        self.rect = pygame.Rect(self.coord.x, self.coord.y, self.boxSize.x, self.boxSize.y)
        
    
    def draw_rect(self, mouse_pos, y) -> None:
        self.rect.y = self.coord.y + y
        
        if self.rect.collidepoint(*mouse_pos):
            color = self.color_selected
        else:
            color = self.color
            
        pygame.draw.rect(self.screen, color, self.rect, border_radius=20)


class RectLobby(RectBase):
    
    def __init__(self, screen: pygame.Surface, nb: str, members: 'tuple[str]', coord: pygame.Vector2) -> None:
        super().__init__(screen, coord, (255, 0, 0), (218, 0, 0))
        self.nb = nb
        self.members = members
    
    def draw(self, mouse_pos, y):
        self.draw_rect(mouse_pos, y)
        
        self.screen.blit(FONT_30.render(f"Lobby {self.nb}", False, (0, 0, 0)), (self.coord.x + 10, self.coord.y + 10 + y))
        for i in range(len(self.members)):
            self.screen.blit(FONT_20.render(self.members[i], False, (255 ,255 ,255)), (self.coord.x + 10, self.coord.y + 50 + i * 25 + y))


class RectNewLobby(RectBase):
    
    def __init__(self, screen: pygame.Surface, coord: pygame.Vector2) -> None:
        super().__init__(screen, coord, (255, 170, 0), (218, 145, 0))
        self.nb = '+'
    
    def draw(self, mouse_pos, y):
        self.draw_rect(mouse_pos, y)
        
        txt = FONT_30.render('+', False, 'white')
        self.screen.blit(txt, (self.coord.x + self.boxSize.x // 2 - txt.get_size()[0] // 2, self.coord.y + self.boxSize.y // 2 - txt.get_size()[1] // 2 + y))