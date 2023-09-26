import customtkinter as ctk
import tkinter as tk

import gui_start_game_menu as gsgm

ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
ctk.set_appearance_mode("dark")


class MainWindow(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        
        self.frame_start_game = gsgm.FrameStartGame(self)
        self.frame_start_game.pack(expand=True, fill='both')


root = MainWindow()

root.mainloop()