import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from pathlib import Path


def generuj_raport(plik_wejsciowy, plik_wyjsciowy):
    try:
        # Odczyt danych wejsciowych
        with open(plik_wejsciowy, 'r') as f:
            dane_wejsciowe = f.read()

        # Odczyt danych wyjsciowych
        with open(plik_wyjsciowy, 'r') as f:
            dane_wyjsciowe = f.read()

        # Data i godzina wykonania
        teraz = datetime.now()
        data_czas = teraz.strftime("%Y-%m-%d %H-%M-%S")
        plik_raportu=data_czas+".pdf"
        projekt_dir = Path(__file__).parent
        subfolder = projekt_dir / 'Raporty'
        subfolder.mkdir(parents=True, exist_ok=True)
        plik_raportu=subfolder / plik_raportu

        #tworzenie raportu PDF
        c = canvas.Canvas(str(plik_raportu), pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(250, 750, "Raport wykonania zadania")
        c.drawString(250, 730, f"Data i godzina: {data_czas}")
        c.drawString(100, 710, "Dane wejsciowe:")
        c.drawString(100, 690, dane_wejsciowe)
        c.drawString(100, 670, "Dane wyjsciowe:")
        c.drawString(100, 650, dane_wyjsciowe)

        c.save()
        print(str(plik_raportu))

    except Exception as e:
        print(f"Wystąpił błąd podczas generowania raportu: {e}")


if __name__ == "__main__":
    plik_wejsciowy = sys.argv[1]
    plik_wyjsciowy = "wyniki.txt"
    generuj_raport(plik_wejsciowy, plik_wyjsciowy)
