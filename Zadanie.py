import tkinter as tk
from tkinter import messagebox
import time
import sys


def aktualizuj_ekran(okno, label, suma, ostateczny=False):
    """
    Aktualizuje wyswietlany dlug sumaryczny w oknie graficznym
    """
    label.config(text=f"Dlug sumaryczny:\n {''.join(map(str, suma))}")
    okno.update()
    time.sleep(0.6)
    if ostateczny:
        okno.after(3000, okno.destroy)

def pomijanie():
    """
    ustawia tryb pomijania wyswietlania zmian długu (przydatne gdy mamy duzo operacji)
    """
    global pomijanie_wyswietlania
    pomijanie_wyswietlania = True
    messagebox.showinfo("Informacja", "Pomijanie wyswietlania wlaczone.")

#Globalna zmienna do kontroli pomijania wyswietlania
pomijanie_wyswietlania = False

def main():

    try:
        #Odczyt danych wejsciowych z pliku
        plik_wejsciowy=sys.argv[1]
        try:
            with open(plik_wejsciowy, 'r') as f:
                dane = f.read().splitlines()
        except Exception as e:
            print("Wystapil blad: ", e)
            return

        #odczyt danych wejsciowych
        n, z = map(int, dane[0].split())  # dlugosc wyswietlacza, liczba operacji
        krajowy = list(map(int,list(dane[1])))  # dlug wewnetrzny
        zagraniczny = list(map(int,list(dane[2])))  #dlug zewnetrzny

        #poczatkowy dlug sumaryczny
        sumaryczny = [0] * n
        for i in range(n - 2,-1,-1):
            sumaryczny[i+1] = int(krajowy[i]) + int(zagraniczny[i])

        #przeniesienie wartosci powyzej 9
        for i in range(n - 1,0,-1):
            if sumaryczny[i] > 9:
                sumaryczny[i] -= 10        # listy sa indeksowane w odwrotnej kolejnosci niz numeracja przyjeta w zadaniu
                if i - 1 >= 0 :
                    sumaryczny[i - 1] += 1
                else:
                    print("Przekroczono rozmiar wyswietlacza")



            #funkcja do  aktualizacji sumarycznego dlugu
        def aktualizuj_sumaryczny(index, delta_krajowy=0, delta_zagraniczny=0):
            przeniesienie = 0
            if delta_krajowy:
                sumaryczny[index] += delta_krajowy
            if delta_zagraniczny:
                sumaryczny[index] += delta_zagraniczny

            # zmiana cyfr i zachowanie przeniesienia
            while index>=0 and index < n:
                if sumaryczny[index] > 9:
                    sumaryczny[index] -= 10
                    przeniesienie = 1
                    if index - 1 >= 0:
                        sumaryczny[index - 1] += przeniesienie
                    index -= 1
                    continue
                elif sumaryczny[index] < 0:
                    sumaryczny[index] += 10
                    przeniesienie = -1
                    if index - 1 >= 0:
                        sumaryczny[index - 1] += przeniesienie
                    index -= 1
                    continue
                else:
                    break




        #tworzenie okna Tkinter do wyswietlania
        global pomijanie_wyswietlania
        okno = tk.Tk()
        okno.title("Dług Bajtocji")
        okno.config(bg="black")
        okno_width = 700
        okno_height = 500
        screen_width = okno.winfo_screenwidth()       #pobieranie wymiarow ekranu
        screen_height = okno.winfo_screenheight()
        # obliczanie pozycji do wysrodkowania
        x_cord = (screen_width // 2) - (okno_width // 2)
        y_cord = (screen_height // 2) - (okno_height // 2)
        okno.geometry(f"{okno_width}x{okno_height}+{x_cord}+{y_cord}")     #ustawianie wynmiarow okna
        label = tk.Label(okno, text=f"Dług sumaryczny:\n {''.join(map(str, sumaryczny))}", font=("Arial", 40), bg="black", fg="lime")
        label.pack(pady=100)
        przycisk = tk.Button(okno, text="Pomiń wyświetlanie", command=pomijanie)
        przycisk.pack(pady=10)


        #obsluga operacji
        wyniki = []
        for linia in dane[3:]:
            operacja = linia.split()
            if operacja[0] == 'W':  #zmiana cyfry dlugu krajowego
                i = n-1 - int(operacja[1])
                c = int(operacja[2])
                delta = c - krajowy[i]
                krajowy[i] = c
                aktualizuj_sumaryczny(i+1, delta_krajowy=delta)
            elif operacja[0] == 'Z':  #zmiana cyfry dlugu zagranicznego
                i = n-1 - int(operacja[1])
                c = int(operacja[2])
                delta = c - zagraniczny[i]
                zagraniczny[i] = c
                aktualizuj_sumaryczny(i+1, delta_zagraniczny=delta)
            elif operacja[0] == 'S':  #zapytanie o cyfre dlugu sumarycznego
                i = n - int(operacja[1])
                wyniki.append(str(sumaryczny[i]))
                #print(wyniki)

            #aktualizacja ekranu po kazdej operacji, jesli tryb wyswietlania jest właczony
            if not pomijanie_wyswietlania:
                aktualizuj_ekran(okno, label, sumaryczny)


        #wyświetlenie końcowego wyniku
        aktualizuj_ekran(okno, label, sumaryczny, ostateczny=True)
        okno.mainloop()


        # Zapis wyników do pliku wyjściowego
        try:
            with open('wyniki.txt', 'w') as f:
                f.write("\n".join(wyniki))
            print("Wyniki zapisane do pliku 'wyniki.txt'.")
        except Exception as e:
            print("Wystapil blad: ", e)





    except Exception as e:
        print("Wystapil blad: ",e)





if __name__ == "__main__":
    main()
