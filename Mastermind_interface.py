from tkinter import ttk
from tkinter import *

class interface():
    def __init__(self):
        self.window = Tk()
        self.window.title("Mastermind")
        self.mainframe = ttk.Frame(self.window)
        self.nr_labels = []
        self.guess_labels = []
        self.cor_pos_labels = []
        self.inc_pos_labels = []

    def init_window(self, game):
        guess_label = Label(self.window, text = "Twój strzał: ")
        guess_label.grid(row = 5, column =2)
        inp = Entry(self.window)
        inp.grid(row = 5, column = 3)
        check = Button(self.window, text = "Sprawdź", command = lambda : self.guess(game, inp))
        reset = Button(self.window, text = "Reset", command = lambda : game.reset())
        cheat = Button(self.window, text = "Oszust", command = lambda : game.cheater())
        
        self.nr_labels.append(Label(self.window, text = "Nr."))

        for i in range(1,game.max_tries+1):
            self.nr_labels.append(Label(self.window, text = str(i)))

        self.guess_labels.append(Label(self.window, text = "Twoje strzały"))
        for i in range(game.max_tries+1):
            self.guess_labels.append(Label(self.window, text = ""))


        self.cor_pos_labels.append(Label(self.window, text = "Poprawne pozycje"))
        for i in range(game.max_tries+1):
            self.cor_pos_labels.append(Label(self.window, text = ""))

        self.inc_pos_labels.append(Label(self.window, text = "Poprawne cyfry na niepoprawnych pozycjach"))
        for i in range(game.max_tries+1):
            self.inc_pos_labels.append(Label(self.window, text = ""))
        

        for x in range(len(self.nr_labels)) :
            self.nr_labels[x].grid(row = x+2, column = 6)
        
        for x in range(len(self.guess_labels)) :
            self.guess_labels[x].grid(row = x+2, column = 7)

        for x in range(len(self.cor_pos_labels)) :
            self.cor_pos_labels[x].grid(row = x+2, column = 8)
        
        for x in range(len(self.inc_pos_labels)) :
            self.inc_pos_labels[x].grid(row = x+2, column = 9)
        
        check.grid(row =5, column =4)
        reset.grid(row = 6, column = 4)
        cheat.grid(row = 7, column = 4)
        self.window.mainloop()

    def quit_two_windows(self, wind):
        wind.destroy()
        self.window.destroy()

    def end_game(self,txt):
        window = Toplevel()
        window.geometry('256x120')
        label = Label(window, text = txt)
        label.pack(fill='x', padx=50, pady=5)

        button_close = Button(window, text="Zamknij", command = lambda : self.quit_two_windows(window))
        button_close.pack(fill='x')

    def reset_labels(self, game):

        for i in range(1,game.max_tries+1):
            self.guess_labels[i]['text'] = ''


        for i in range(1,game.max_tries+1):
            self.cor_pos_labels[i]['text'] = ''

        for i in range(1,game.max_tries+1):
            self.inc_pos_labels[i]['text'] = ''

    def guess(self, game, inp):
        string = inp.get()
        game.guess(string)
        inp.delete(0, len(string))

    def inc_code(self, txt):
        window = Toplevel()
        window.geometry('300x120')
        label = Label(window, text = txt)
        label.pack(fill='x', padx=50, pady=5)

        button_close = Button(window, text="Zamknij", command = lambda : window.destroy())
        button_close.pack(fill='x')