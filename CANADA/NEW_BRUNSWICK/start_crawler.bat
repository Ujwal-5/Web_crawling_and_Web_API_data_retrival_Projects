@echo off
:loop
python canbreg_crawling.py
timeout /t 300
goto loop