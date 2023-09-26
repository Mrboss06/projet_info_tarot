import customtkinter as ctk
import tkinter as tk

players = ['', 'Loic', 'Jean Raphael', 'Etienne', 'Damien']
prise = ['', 'Petite', 'Garde', 'Garde-sans', 'Garde-contre']

class FrameNouvelleDonne(ctk.CTkFrame):
    
    def __init__(self, master):
        super().__init__(master)
        
        self.frame_prem_ligne = ctk.CTkFrame(self)
        self.frame_prem_ligne.pack()
        
        self.frame_deux_ligne = ctk.CTkFrame(self)
        self.frame_deux_ligne.pack()
        
        # le texte "Annonce:"
        self.label1 = ctk.CTkLabel(self.frame_prem_ligne, text="Annonce:")
        self.label1.pack(side="left")
        
        # le menu deroulant pour choisir le preneur
        self.preneurOptionMenu = ctk.CTkOptionMenu(self.frame_prem_ligne, values=players)
        self.preneurOptionMenu.pack(side="left")
        
        # le texte "a fait une"
        self.label2 = ctk.CTkLabel(self.frame_prem_ligne, text='a fait une')
        self.label2.pack(side="left")
        
        # le menu deroulant pour choisir la prise
        self.priseOptionMenu = ctk.CTkOptionMenu(self.frame_prem_ligne, values=prise)
        self.priseOptionMenu.pack(side="left")
        
        # le texte "Il a fait" combien de points
        self.label3 = ctk.CTkLabel(self.frame_deux_ligne, text='Il a fait')
        self.label3.pack(side='left')
        
        # l'entree pour mettre le nombre de point fait
        self.nbPointEntry = ctk.CTkEntry(self.frame_deux_ligne)