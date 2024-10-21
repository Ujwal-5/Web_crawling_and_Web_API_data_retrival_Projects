@echo off
call env/Scripts/activate.bat
:loop
python  ./minnesota_crawling.py
timeout /t 60
goto loop