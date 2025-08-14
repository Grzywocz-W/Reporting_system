import sys
import pikepdf
from pathlib import Path


def utworz_backup(raport, plik_backup):
    try:
        if not raport:
            print("Brak pliku PDF do utworzenia backupu.")
            return

        if plik_backup.exists():
            with pikepdf.open(str(plik_backup),allow_overwriting_input=True) as backup_pdf:
                with pikepdf.open(str(raport)) as pdf:
                    # Dopisujemy strony do istniejacego pliku backupu
                    backup_pdf.pages.extend(pdf.pages)
                # Zapisujemy nowy backup z dodanymi stronami
                backup_pdf.save(str(plik_backup))
                print(f"Raport został dodany do pliku backup: {plik_backup}")
        else:
            with pikepdf.Pdf.new() as backup_pdf:
                with pikepdf.open(str(raport)) as pdf:
                    # Dopisujemy strony do nowego pliku backupu
                    backup_pdf.pages.extend(pdf.pages)
                # Zapisujemy nowy backup z dodanymi stronami
                backup_pdf.save(str(plik_backup))
                print(f"Raport został dodany do pliku backup: {plik_backup}")

    except Exception as e:
        print(f"Wystąpił błąd podczas tworzenia backupu: {e}")


if __name__ == "__main__":
    raport = sys.argv[1]
    projekt_dir = Path(__file__).parent
    plik_backup = projekt_dir / 'Backup.pdf'
    utworz_backup(raport, plik_backup)
