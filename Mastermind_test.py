#Wersja programu użyta do testowania 

from abc import ABC, abstractmethod
import random
from tkinter import *
import Mastermind_interface

#klasy wyjątków 

#wyjątek odpowiadający za zakończenie gry
class GameEnd(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value) 

#wyjątek odpowiadający za obsługę kodu w błędnym formacie
class IncorrectCode(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

#wyjątek odpowiadający za reset gry
class Reset(Exception):
    def __init__(self):
        pass
         
#abstrakcyjna klasa bazowa po której dziedziczą obie wersje gry
class RegulyGry(ABC):
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def cheater(self):
        pass

    @abstractmethod
    def guess():
        pass
    
    @abstractmethod
    def check_guess():
        pass
    
    @abstractmethod
    def feedback():
        pass
    @abstractmethod
    def reset():
        pass

#zwykła wersja gry mastermind
class regular_mastermind(RegulyGry):
    
    #konstruktor
    def __init__(self, inter):
        self.code_len = 4                                               #zdefiniowanie długości kodu
        self.code = [random.randint(1,6) for i in range(self.code_len)] #generacja kodu
        self.tries = 0                                                  #zmienna przetrzymująca ilość wykorzystanych prób
        self.u_guesses = []                                             #zdefiniowanie tablic przetrzymuących strzały gracza
        self.u_guesses_positions = []                                   #oraz ilość cyfr na poprawnych/niepoprawnych miejscach 
        self.max_tries =12                                              #zdefiniowanie maksymalnej ilości prób
        self.interface = inter

    def play(self):
        self.interface.init_window(self)

    def test(self):
        print("Poprawny kod: " + str(self.code))
        self.interface.init_window(self)

    def cheater(self):
        self.interface.end_game("Tere fere")
        exit
        
    #fukcja która odbiera dane wejściowe, waliduje je oraz zapisuje    
    def guess(self, u_guess_str):
        try:
            if (self.tries<self.max_tries):                                 #walidacja ilości prób
                u_guess = list(u_guess_str)                                 #zmiana danych wejściowych z string na listę 
                if not (u_guess_str.isnumeric()):                           #sprawdzenie czy dane wejściowe składają się z cyfr
                    raise IncorrectCode(self.code_len)
                elif len(u_guess_str) != self.code_len:                     #walidacja długości danych wejściowych
                    raise IncorrectCode(self.code_len)
                else:
                    for i in u_guess:                                       #sprawdzenie czy dane wejściowe składają się z cyfr z przedziału [1,6]
                        if int(i)==0 or int(i)>6:
                            raise IncorrectCode(self.code_len)
                    else:
                        self.u_guesses.append(u_guess.copy())               #zapis strzału gracza 
                        self.tries += 1
                        self.check_guess()                                     #zwiększenie licznika wykorzystanych prób
            else:
                raise GameEnd("Przegrana")                                  #zakończenie gry w wypadku wyczerpania prób
        except GameEnd as end:
            self.interface.end_game("\n" + end.value + "\npoprawny kod: " + str(self.code))         #obsługa zakończenia gry
            print("\n",end)
            print("poprawny kod: " +  str(self.code)) 
        except IncorrectCode as inc:                            #obsługa błednie wpisanego strzału
            self.interface.inc_code("Kod musi składać się z " + str(inc) +" cyfr 1-6")  
    
    #funkcja sprawdzająca strzał gracza                
    def check_guess(self):
        try:
            incor_positions = 0                                                #ilość poprawnych cyfr na niepoprawnych miejscach                  
            cor_positions = 0                                                  #ilość poprawnych cyfr na poprawnych miejscach
            outi = []                                                          #tablica przetrzymująca ideksy zweryfikowanych cyfr kodu 
            outj = []                                                          #tablica przetrzymująca ideksy zweryfikowanych cyfr kodu
            for i in range(len(self.u_guesses[self.tries-1])):                 #sprawdzanie ilości poprawnych cyfr na poprawnych miejscach
                if int(self.u_guesses[self.tries-1][i]) == self.code[i]:
                    cor_positions += 1
                    outi.append(i)
                    outj.append(i)
            if cor_positions == self.code_len:
                raise GameEnd("Wygrana")
            for i in range(len(self.u_guesses[self.tries-1])):                  #sprawdzenie ilości poprawnych cyfr na niepoprawnych miejscach
                for j in range(len(self.u_guesses[self.tries-1])):
                    if ((int(self.u_guesses[self.tries-1][i]) == self.code[j]) and not j in outj and i not in outi):
                        incor_positions += 1
                        outj.append(j)
                        outi.append(i)
            self.u_guesses_positions.append([incor_positions,cor_positions])    #zapisanie ilości poprawnych cyfr na niepoprwanych i poprawnych pozycjach
            self.feedback()
        except GameEnd as end:                                                  #obsługa zakończenia gry 
            print("\n",end)
            self.interface.end_game(end.value)

    #wypisanie informacji o ilości cyfr na poprawnych oraz niepoprawnych miejscach
    def feedback(self):
        self.interface.guess_labels[self.tries]['text'] = str (self.u_guesses[self.tries-1])
        self.interface.cor_pos_labels[self.tries]['text'] = str(self.u_guesses_positions[self.tries-1][1])
        self.interface.inc_pos_labels[self.tries]['text'] = str(self.u_guesses_positions[self.tries-1][0])
        print("Wpisany kod: ", self.u_guesses[self.tries-1], 
              "\nIlość poprawnych cyfr na niepoprawnych miejscach: ", str(self.u_guesses_positions[self.tries-1][0]),  
              "\nIlość poprawnych cyfr na poprawnych miejscach: ", str(self.u_guesses_positions[self.tries-1][1]))

    #funkcja resetująca grę
    def reset(self):
        print("Reset")
        self.code = [random.randint(1,6) for i in range(self.code_len)]     #ponowna generacja kodu
        self.tries = 0                                                      #wyzerowanie wykorzystanych prób
        self.u_guesses = []                                                 #wyzerowanie tablic przetrzymuących poprzednie strzały gracza 
        self.u_guesses_positions = []                                       #oraz ilość cyfr na poprawnych/niepoprawnych miejscach w poprzednich strzałach
        self.interface.reset_labels(self)

#oszukująca wersja gry mastermind
class cheating_mastermind(RegulyGry):
    #kontruktor
    def __init__(self, inter):
        self.code_len = 4                                               #zdefiniowanie długości kodu
        self.tries = 0                                                  #zmienna przetrzymująca ilość wykorzystanych prób
        self.u_guesses = []                                             #zdefiniowanie tablic przetrzymuących strzały gracza
        self.u_guesses_positions = []                                   #oraz ilość cyfr na poprawnych/niepoprawnych miejscach 
        self.max_tries =12                                              #zdefiniowanie maksymalnej ilości prób
        self.interface = inter

    def play(self):
        self.interface.init_window(self)

    def test(self):
        print("Jestem oszustem")
        self.interface.init_window(self)

    def cheater(self):
        self.interface.end_game("Złapałeś/aś mnie")
        print("Złapałeś/aś mnie") 
    
    #fukcja która odbiera dane wejściowe, waliduje je oraz zapisuje 
    def guess(self, u_guess_str):
        try:
            if (self.tries<self.max_tries):                                 #walidacja ilości prób
                u_guess = list(u_guess_str)                                 #zmiana danych wejściowych z string na listę 
                if not (u_guess_str.isnumeric()):                           #sprawdzenie czy dane wejściowe składają się z cyfr
                    raise IncorrectCode(self.code_len)
                elif len(u_guess_str) != self.code_len:                     #walidacja długości danych wejściowych
                    raise IncorrectCode(self.code_len)
                else:
                    for i in u_guess:                                       #sprawdzenie czy dane wejściowe składają się z cyfr z przedziału [1,6]
                        if int(i)==0 or int(i)>6:
                            raise IncorrectCode(self.code_len)
                    else:
                        self.u_guesses.append(u_guess.copy())               #zapis strzału gracza 
                        self.tries += 1
                        self.check_guess()                                     #zwiększenie licznika wykorzystanych prób
            else:
                raise GameEnd("Przegrana")                                  #zakończenie gry w wypadku wyczerpania prób
        except GameEnd as end:
            self.interface.end_game("\n" + end.value)                                  #obsługa zakończenia gry
            print("\n",end)
        except IncorrectCode as inc:                            #obsługa błednie wpisanego strzału
            print("Kod musi składać się z ",inc," cyfr 1-6")
            self.interface.inc_code("Kod musi składać się z " + str(inc) +" cyfr 1-6") 

    #funkcja generująca losowe wartości liczby cyfr na poprawnych/niepoprawnych miejscach
    def check_guess(self):
        cor_positions = random.randint(0,self.code_len)                   #generowanie losowej liczby poprawnych cyfr na poprawnych pozycjach, mniejszej od długości kodu
        incor_positions = random.randint(0,self.code_len-cor_positions)   #generowanie losowej liczby poprawnych cyfr na niepoprawnych pozycjach, mniejszej od różnicy długości kodu oraz liczby poprawnych cyfr na poprawnych pozycjach 
        self.u_guesses_positions.append([incor_positions,cor_positions])    #zapisanie wygenerowanych liczb
        self.feedback()

    #wypisanie informacji o wygenerowanej liczbie cyfr na poprawnych oraz niepoprawnych miejscach
    def feedback(self):
        self.interface.guess_labels[self.tries]['text'] = str (self.u_guesses[self.tries-1])
        self.interface.cor_pos_labels[self.tries]['text'] = str(self.u_guesses_positions[self.tries-1][1])
        self.interface.inc_pos_labels[self.tries]['text'] = str(self.u_guesses_positions[self.tries-1][0])
        print("Wpisany kod: ", self.u_guesses[self.tries-1], 
              "\nIlość poprawnych cyfr na niepoprawnych miejscach: ", str(self.u_guesses_positions[self.tries-1][0]),  
              "\nIlość poprawnych cyfr na poprawnych miejscach: ", str(self.u_guesses_positions[self.tries-1][1]))

    #funkcja resetująca grę    
    def reset(self):
        self.tries = 0                      #wyzerowanie liczby wykorzystanych prób
        self.u_guesses = []                 #wyzerowanie tablic przetrzymuących poprzednie strzały gracza 
        self.u_guesses_positions = []       #oraz ilość cyfr na poprawnych/niepoprawnych miejscach w poprzednich strzałach
        self.interface.reset_labels(self)

#funkcja inicjująca grę        
def start_game():
    cheat_chance = 0.3                      #zdefiniowanie szansy na oszukującą grę
    x = random.random()
    inter = Mastermind_interface.interface()
    if x > cheat_chance:                    #wybór między normalną oraz oszukującą grą
        new_game = regular_mastermind(inter)
    else:
        new_game = cheating_mastermind(inter)
    new_game.play()

#funkcja inicjująca grę        
def test_game():
    cheat_chance = 0.3                      #zdefiniowanie szansy na oszukującą grę
    x = random.random()
    inter = Mastermind_interface.interface()
    if x > cheat_chance:                    #wybór między normalną oraz oszukującą grą
        new_game = regular_mastermind(inter)
    else:
        new_game = cheating_mastermind(inter)
    new_game.test()

test_game()                