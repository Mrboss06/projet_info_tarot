import customtkinter as ctk
import tkinter as tk

import gui_nouvelle_donne as gnd


ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
ctk.set_appearance_mode("dark")

root = ctk.CTk()

a = gnd.FrameNouvelleDonne(root)
a.pack()




root.mainloop()