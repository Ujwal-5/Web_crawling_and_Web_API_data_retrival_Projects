@echo off
call Scripts/activate.bat
:loop
python  ./xsmucbrdx_update_comp_crawling_X.py
aws s3 mv ReportsX/ s3://prod_buk/DATA/XSMUCBRDX/BULK/TODO/ --recursive
timeout /t 1000
goto loop