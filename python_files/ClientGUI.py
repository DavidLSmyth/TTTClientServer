from TTTClient import TTTClient
import tkinter as tk

class TTTClientGUI(TTTClient):
    def __init__(self, parent):
        self.parent = parent
        self.parent.resizable(width=tk.FALSE, height=tk.FALSE)
        self.parent.title("TicTacToe")
        self.parent.configure(bg="black")
        self.difficulty = tk.StringVar(self.parent)
        self.difficulty.set("hard")
        self.optionmenu = tk.OptionMenu(root, self.difficulty, "easy", "hard")
        self.optionmenu.configure(bg="khaki")
        self.optionmenu.grid(row=3, column=2)

    def get_input(self):
        #get input from GUI
        pass

    def my_turn(self):
        #get input from GUI then call regular my_turn
        super().my_turn()
