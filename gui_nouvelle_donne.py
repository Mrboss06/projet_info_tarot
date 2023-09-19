import customtkinter as ctk
import tkinter as tk

class FrameNouvelleDonne(ctk.CTkFrame):
    
    def __init__(self, master):
        super().__init__(master)
        self.labelPreneur = ctk.CTkLabel(self)
        self.labelPreneur.pack()