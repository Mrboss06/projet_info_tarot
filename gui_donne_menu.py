import customtkinter as ctk
import tkinter as tk

import gui_nouvelle_donne as gnd

class FrameDonne(ctk.CTkFrame):
    
    def __init__(self, master):
        super().__init__(master)
        
        self.donneHolder = ctk.CTkFrame(self)
        self.donneHolder.pack()
        
        self.donnes = []
        
        self.donnes.append(gnd.FrameNouvelleDonne(self.donneHolder))
        self.donnes[-1].pack(expand=True, side='left')