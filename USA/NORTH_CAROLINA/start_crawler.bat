@echo off
call env/Scripts/activate.bat
:loop
python  ./north_carolina.py
timeout /t 60
goto loop