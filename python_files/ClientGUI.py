from TTTClient import TTTClient
import tkinter as tk
#this is a view
class TTTClientGUI(TTTClient):
    def __init__(self, parent):
        self.parent = parent
        self.parent.resizable(width=tk.FALSE, height=tk.FALSE)
        self.parent.title("TicTacToe")
        self.parent.configure(bg="black")
        self.optionmenu = tk.OptionMenu(self.parent, self.difficulty, "easy", "hard")
        self.optionmenu.configure(bg="khaki")

    def get_input(self):
        #get input from GUI
        pass

    def my_turn(self):
        #get input from GUI then call regular my_turn
        super().my_turn()
