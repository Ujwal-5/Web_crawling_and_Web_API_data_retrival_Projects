@echo off
call env/Scripts/activate.bat
:loop
python  ./nif_extraction.py
timeout /t 60
goto loop