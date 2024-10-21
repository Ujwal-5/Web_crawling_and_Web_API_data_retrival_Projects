@echo off
:loop
aws s3 mv C:\wamp64\www\XSUSREG\json s3://dev_buk/DATA/XSUSREG/US-OH/BULK_JSON/ --recursive
aws s3 mv C:\wamp64\www\XSUSREG\company_json s3://dev_buk/DATA/XSUSREG/US-OH/JSON/ --recursive
timeout /t 60
goto loop