import requests
import time
import random
from database import DbService
from s3_move import move_files
from moniter import hit_moniter_api
from folder import create_folder
from custom_request import make_request_with_retry
from save_file import save_html_file
from settings import AWS, MYSQL
from bs4 import BeautifulSoup
import urllib.parse
import re
from urllib.parse import urlparse

folder_name = 'html'
create_folder(folder_name=folder_name)

local_path = f'./{folder_name}/'
s3_path = f"s3://{AWS['bucket']}/DATA/{AWS['source']}/{AWS['folder']}/"
move_files(local_path, s3_path)

#Update table
table_name = MYSQL['table']
procedure_name = MYSQL['procedure']
procedure_parameter = MYSQL['procedure_parameter']
column_name = 'company_number'
status_column = 'STATUS'

for _ in range(50):
    print('Script Started!')
    hit_moniter_api('hawaii_moniter.json')
    time.sleep(random.uniform(3, 6))
    keyword = DbService().get_a_record(procedure_name, parameter=procedure_parameter)

    result_response = make_request_with_retry(url = f"https://hbe.ehawaii.gov/documents/business.html?fileNumber={keyword}&view=documents", session=requests, method='get', headers=None, data=None, max_retries=5, retry_delay=3)
    time.sleep(random.uniform(3, 6))
    if "Page not found" in (result_response.text):
        result_response = make_request_with_retry(url = f"https://hbe.ehawaii.gov/documents/temporary.html?fileNumber={keyword}", session=requests, method='get', headers=None, data=None, max_retries=5, retry_delay=3)

    print(result_response.text)
    if "All Company Info" in result_response.text:
        save_html_file(folder_name=folder_name, keyword=keyword, html_content=result_response.text)
        DbService().update_the_record(status =10, table=table_name, column=column_name, status_column=status_column,  keyword=keyword)
    else:
        print("No data or error")
        DbService().update_the_record(status =5, table=table_name, column=column_name, status_column=status_column,  keyword=keyword)
    time.sleep(random.uniform(3,12))
move_files(local_path, s3_path)

