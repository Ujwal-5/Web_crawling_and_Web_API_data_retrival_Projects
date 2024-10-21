@echo off

REM Create virtual environment
python -m venv env

REM Activate virtual environment
call env/Scripts/activate.bat

REM Install dependencies
pip install -r requirements.txt

REM Run your Python script
python nif_extraction.py

REM Deactivate virtual environment
deactivate
