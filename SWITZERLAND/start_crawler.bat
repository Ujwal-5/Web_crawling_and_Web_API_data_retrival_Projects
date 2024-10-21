@echo off
call env/Scripts/activate.bat
:loop
python  ./xschregx_crawling.py
timeout /t 60
goto loop