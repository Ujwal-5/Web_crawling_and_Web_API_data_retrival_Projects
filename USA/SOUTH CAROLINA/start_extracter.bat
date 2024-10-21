@echo off
call env/Scripts/activate.bat
:loop
python  ./minnesota_extraction.py
timeout /t 60
goto loop