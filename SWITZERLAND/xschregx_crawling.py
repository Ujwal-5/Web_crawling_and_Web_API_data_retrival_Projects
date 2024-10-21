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
column_name = 'uidFormatted'
status_column = 'STATUS'


for _ in range(50):
    print('Script Started!')
    hit_moniter_api('xschregx_moniter.json')
    time.sleep(random.uniform(3, 6))
    urls = DbService().get_a_record(procedure_name, parameter=procedure_parameter)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Host': 'sh.chregister.ch',
        'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    home_response = make_request_with_retry(url = urls, session=requests, method='get', headers=headers, data=None, max_retries=5, retry_delay=3)
    time.sleep(random.uniform(3, 6))
    cookies = home_response.cookies
    cookie_string = '; '.join([f"{cookie.name}={cookie.value}" for cookie in cookies])
    print('cookie =', cookie_string)
    soup = BeautifulSoup(home_response.text, 'html.parser')
    input_tag = soup.find('input', {'name': 'javax.faces.ViewState'})
    if input_tag:
        value = input_tag.get('value')
        print("Value:", value)
        encoded_value = urllib.parse.quote(value)
        print(encoded_value, "encoded value")
    else:
        print("No input tag found with name 'javax.faces.ViewState'")

    nonce_pattern = r'nonce="([^"]+)"'
    matches = re.findall(nonce_pattern, home_response.text)
    if matches:
        nonce_value = matches[0]
        print("Nonce value:", nonce_value)
    else:
        print("No nonce value found in the JavaScript string.")

    payload1 = f'javax.faces.partial.ajax=true&javax.faces.source=idAuszugForm%3AauszugContentPanel&primefaces.ignoreautoupdate=true&javax.faces.partial.execute=idAuszugForm%3AauszugContentPanel&javax.faces.partial.render=idAuszugForm%3AauszugContentPanel&idAuszugForm=auszugContentPanel%3AidAuszugForm%3AauszugContentPanel&idAuszugForm=auszugContentPanel_load%3Atrue&idAuszugForm=idAuszugForm&javax.faces.ViewState={encoded_value}&primefaces.nonce={nonce_value}'
    headers1 = {
    'Accept': 'application/xml, text/xml, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    # 'Content-Length': '508',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': cookie_string,
    'Faces-Request': 'partial/ajax',
    # 'Host': 'sh.chregister.ch',
    # 'Origin': 'https://sh.chregister.ch',
    'Referer': urls,
    'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
    }
    
    parsed_url = urlparse(urls)
    base_url = parsed_url.scheme+"://"+parsed_url.netloc+parsed_url.path
    keyword = parsed_url.query.split("=")[1]
    result_response = make_request_with_retry(url=base_url, session=requests, method='post', headers=headers1, data=payload1, max_retries=5, retry_delay=3)
    print(result_response.text)
    if "Business name" in result_response.text:
        save_html_file(folder_name=folder_name, keyword=keyword, html_content=result_response.text)
        DbService().update_the_record(status =10, table=table_name, column=column_name, status_column=status_column,  keyword=urls)
    else:
        print("No data or error")
        DbService().update_the_record(status =5, table=table_name, column=column_name, status_column=status_column,  keyword=urls)

move_files(local_path, s3_path)

