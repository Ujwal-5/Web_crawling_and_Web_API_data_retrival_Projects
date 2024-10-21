@echo off
:loop
aws s3 mv C:\Scripts\Nicaragua\JSON\ s3://dev_buk/DATA/SOURCE/NICARAGUA/JSONS/ --recursive
timeout /t 60
goto loop