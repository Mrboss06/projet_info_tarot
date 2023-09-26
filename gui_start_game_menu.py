import customtkinter as ctk
import tkinter as tk


class FrameStartGame(ctk.CTkFrame):
    
    def __init__(self, master):
        super().__init__(master)
        
        # le texte "Joueurs"
        self.playerLabel = ctk.CTkLabel(self, text='Joueurs:')
        self.playerLabel.pack()
        
        # la frame qui prend toutes les entrées des noms des joueurs
        self.playerHolder = ctk.CTkFrame(self)
        self.playerHolder.pack(expand=True, fill='x')
        
        # liste avec les frame de chaque entrée de joueur
        self.players = []
        for player in range(4):
            '''
            Une liste qui contient la frame du joueur et la variable du joueur
            chaque frame de joueur contient:
            - un label "Player Nr X"
            - une entrée pour recevoir le nom du joueur
            la variable contient le nom du joueur donné
            '''
            playerList = []
            playerList.append(ctk.CTkFrame(self.playerHolder))
            
            # la variable qui stock le nom du joueur numero 'player'
            playerList.append(tk.StringVar())
            
            ctk.CTkLabel(playerList[0], text="Player "+str(player+1)).grid(column=0, row=0)
            ctk.CTkEntry(playerList[0], textvariable=playerList[-1]).grid(column=1, row=0, padx=10, pady=10)
            
            playerList[0].pack()
            
            self.players.append(playerList)
            
            
        
        self.buttonHolder = ctk.CTkFrame(self)
        self.buttonHolder.pack(expand=True, fill='x')
        
        self.PlayButton = ctk.CTkButton(self.buttonHolder, text='Start Game', command=self.get_players_name)
        self.PlayButton.pack()
    
    def get_players_name(self):
        players_name = []
        for player in range(4):
            players_name.append(self.players[player][-1].get())
        print(players_name)