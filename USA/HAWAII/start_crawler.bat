@echo off
call env/Scripts/activate.bat
:loop
python hawaii_crawling.py
timeout /t 60
goto loop