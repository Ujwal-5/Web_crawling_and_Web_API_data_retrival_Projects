@echo off
call Scripts/activate.bat
:loop
python  ./xsmucbrd_update_comp_crawling.py
aws s3 mv Reports/ s3://prod_buk/DATA/XSMUCBRD/TODO/ --recursive
timeout /t 1000
goto loop