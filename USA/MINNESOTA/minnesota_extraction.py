import requests
import time
import random
from database import DbService
from moniter import hit_moniter_api
from folder import create_folder
from custom_request import make_request_with_retry
from settings import AWS, MYSQL
import re

folder_name = 'html'
create_folder(folder_name=folder_name)
local_path = f'./{folder_name}/'
s3_path = f"s3://{AWS['bucket']}/DATA/{AWS['source']}/{AWS['folder']}/"
table_name = MYSQL['table_keyword']
procedure_name = MYSQL['procedure_keyword']
procedure_parameter = MYSQL['procedure_parameter']
column_name = 'KEYWORD'
status_column = 'FLAG'

for _ in range(50):
    print('Script Started!')
    hit_moniter_api('minnesota_extract_moniter.json')
    time.sleep(random.uniform(3, 6))
    keyword = DbService().get_a_record(procedure_name, parameter=procedure_parameter)
    list_response = make_request_with_retry(url = f'https://mblsportal.sos.state.mn.us/Business/BusinessSearch?BusinessName={keyword}&IncludePriorNames=False&Status=Active&Type=BeginsWith', session=requests, method='get', headers=None, data=None, max_retries=5, retry_delay=3)
    time.sleep(random.uniform(3, 6))
    # print(list_response.text.encode('utf-8'))
    filing_guid_list = []
    pattern = r'filingGuid=([a-f0-9-]+)'
    matches = re.findall(pattern, str(list_response.text))

    if matches:
        for match in matches:
            filing_guid_list.append(match)
            
    else:
        print("No match found.")

    print(filing_guid_list)
    
    if filing_guid_list != []:
        DbService().insert_the_record(insert_column='URL_MINNESOTA', insert_list=filing_guid_list)
        DbService().update_the_record(status =10, table=table_name, column=column_name, status_column=status_column,  keyword=keyword)
    else:
        print("No data or error")
        DbService().update_the_record(status =5, table=table_name, column=column_name, status_column=status_column,  keyword=keyword)


