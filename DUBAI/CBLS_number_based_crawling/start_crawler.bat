@echo off
:loop
python xsaener_crawling_16.py	
timeout /t 180
goto loop