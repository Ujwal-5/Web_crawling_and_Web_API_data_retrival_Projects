import requests
import time
import random
from database import DbService
from moniter import hit_moniter_api
from custom_request import make_request_with_retry
from settings import MYSQL
import re

table_name = MYSQL['table_keyword']
procedure_name = MYSQL['procedure_keyword']
procedure_parameter = MYSQL['procedure_parameter']
column_name = 'KEYWORD'
status_column = 'FLAG'

for _ in range(50):
    print('Script Started!')
    hit_moniter_api('wisconsin_extract_moniter.json')
    time.sleep(random.uniform(3, 6))
    keyword = DbService().get_a_record(procedure_name, parameter=procedure_parameter)
    list_response = make_request_with_retry(url = f'https://www.wdfi.org/apps/CorpSearch/Results.aspx?type=Simple&q={keyword}', session=requests, method='get', headers=None, data=None, max_retries=5, retry_delay=3)
    time.sleep(random.uniform(3, 6))
    # print(list_response.text.encode('utf-8'))
    entityid_list = []
    pattern = r'Details\.aspx\?entityID=([A-Za-z0-9]+)&hash=([0-9]+)'
    matches = re.findall(pattern, str(list_response.text))

    if matches:
        for match in matches:
            entityid, hash_value= match
            entityid_list.append(f'{entityid}_{hash_value}')
            
    else:
        print("No match found.")

    # print(entityid_list)
    
    if entityid_list != []:
        DbService().insert_the_record(insert_column='URL_WISCONSIN', insert_list=entityid_list)
        DbService().update_the_record(status =10, table=table_name, column=column_name, status_column=status_column,  keyword=keyword)
    else:
        print("No data or error")
        DbService().update_the_record(status =5, table=table_name, column=column_name, status_column=status_column,  keyword=keyword)


