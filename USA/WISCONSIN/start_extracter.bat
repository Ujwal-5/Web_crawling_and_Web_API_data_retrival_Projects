@echo off
:loop
wisconsin_extraction.exe
timeout /t 60
goto loop