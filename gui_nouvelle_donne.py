import customtkinter as ctk
import tkinter as tk

players = ['', 'Loic', 'Jean Raphael', 'Etienne', 'Damien']
prise = ['', 'Petite', 'Garde', 'Garde-sans', 'Garde-contre']

class FrameNouvelleDonne(ctk.CTkFrame):
    
    def __init__(self, master):
        super().__init__(master)
        
        self.frame_prem_ligne = ctk.CTkFrame(self)
        self.frame_prem_ligne.pack(anchor='w')
        
        self.frame_deux_ligne = ctk.CTkFrame(self)
        self.frame_deux_ligne.pack(anchor='w')
        
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
        
        # le texte "Il avait" combien de bouts
        self.label3 = ctk.CTkLabel(self.frame_deux_ligne, text='Il avait')
        self.label3.pack(side='left')
        
        
        # l'entree pour mettre le nombre de bouts
        self.nbBoutsEntry = ctk.CTkOptionMenu(self.frame_deux_ligne, values=[0, 1, 2, 3])
        self.nbBoutsEntry.pack(side='left')
        
        
        # le texte "bouts et avait" combien de points
        self.label4 = ctk.CTkLabel(self.frame_deux_ligne, text='bouts et a fait')
        self.label4.pack(side='left')
        
        
        self.nbPointsVar = tk.StringVar()
        
        # l'entrée pour mettre le nombre de point
        self.nbPointsEntry = ctk.CTkEntry(self.frame_deux_ligne, textvariable=self.nbPointsVar)
        self.nbPointsEntry.pack(side='left')
