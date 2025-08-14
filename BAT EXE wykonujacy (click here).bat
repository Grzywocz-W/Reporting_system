@echo off
REM Skrypt do zarządzania zadaniem, raportem i backupem

cd /d %~dp0

set /p "WEJSCIE=Podaj plik w ktorym masz dane wejsciowe (np.dane.txt lub pelna sciezka): "

echo.

call python Zadanie.py "%WEJSCIE%"

for /f "delims=" %%i in ('python Raport.py "%WEJSCIE%"') do set "nowy_raport=%%i"
setlocal enabledelayedexpansion
echo Nowy raport zapisano w pliku pdf: !nowy_raport!

call python Backup.py "!nowy_raport!"

echo Wszystkie operacje wykonano pomyslnie.
echo.
echo.
pause