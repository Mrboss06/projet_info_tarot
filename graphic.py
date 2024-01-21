import pygame
import sys
import graphic_choisir_lobby
import graphic_choisir_pseudo
import graphic_attente_dans_lobby
import graphic_tour_de_jeu
from joueur import Joueur
from graphic_constant import SCREEN_HEIGHT, SCREEN_WIDTH, CARD_SIZE


pygame.init()
pygame.font.init()



class Window:
    def __init__(self, joueur: Joueur) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.SysFont('Roboto', 50)
        
        self.cardsImg = {}
        for card in ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A13", "A14", "A15", "A16", "A17", "A18", "A19", "A20", "A21", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C14", "K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8", "K9", "K10", "K11", "K12", "K13", "K14", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10", "P11", "P12", "P13", "P14", "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12", "T13", "T14"]:
            self.cardsImg[card] = pygame.image.load(f"assets/cards/{card}.png")
            self.cardsImg[card] = pygame.transform.scale(self.cardsImg[card], CARD_SIZE)
        
        self.tab_choose_username = graphic_choisir_pseudo.TabChooseUsername(self.screen)
        self.tab_select_lobby = graphic_choisir_lobby.TabSelectLobby(self.screen)
        self.tab_waiting_in_lobby = graphic_attente_dans_lobby.WaitingInLobby(self.screen)
        self.tab_tour_de_jeu = graphic_tour_de_jeu.TourDeJeu(self.screen, self.cardsImg)
        self.menu = ''
        self.joueur = joueur

    def run(self):
        running = True
        while running:
            
            self.screen.fill((0,0,0))
            
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            
            mouse_pos = pygame.mouse.get_pos()
            
            #rect_with_mouse(pygame.Rect.collidepoint(rect, *mouse_pos))
            #pygame.draw.rect(screen, (255,0,0), rect)
            
            if self.menu == 'username':
                self.screen.blit(self.font.render("Ton pseudo", False, (255,255,255)), (50, 100))
                self.tab_choose_username.choisir_pseudo(events)
            elif self.menu == 'choisir_lobby':
                self.tab_select_lobby.selectionner_lobby(events, mouse_pos)
            elif self.menu == 'attente_dans_lobby':
                self.tab_waiting_in_lobby.draw()
            elif self.menu == 'tour_de_jeu':
                self.tab_tour_de_jeu.update(events, mouse_pos, self.joueur.main)
            else:
                self.screen.blit(self.font.render("En attente", False, (255, 255, 255)), (60, 60))
            
            
            pygame.display.update()

        pygame.quit()