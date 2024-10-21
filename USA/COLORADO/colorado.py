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

folder_name = 'html'
create_folder(folder_name=folder_name)

#Update table
table_name = MYSQL['table']
procedure_name = MYSQL['procedure']
procedure_parameter = MYSQL['procedure_parameter']
column_name = 'company_number'
status_column = 'STATUS'

for _ in range(50):
    print('Script Started!')
    hit_moniter_api('colorado.json')
    time.sleep(random.uniform(3, 6))
    keyword = DbService().get_a_record(procedure_name, parameter=procedure_parameter)
    session = requests.Session()
    enity_response = make_request_with_retry(url = f'https://www.sos.state.co.us/biz/BusinessEntityDetail.do?quitButtonDestination=BusinessEntityResults&nameTyp=ENT&masterFileId={keyword}&entityId2={keyword}&fileId=&srchTyp=ENTITY', session=session, method='get', headers=None, data=None, max_retries=5, retry_delay=3)
    entity_history = make_request_with_retry(url = f'https://www.sos.state.co.us/biz/BusinessEntityHistory.do?quitButtonDestination=BusinessEntityDetail&pi1=1&nameTyp=ENT&masterFileId={keyword}&entityId2=&srchTyp=', session=session, method='get', headers=None, data=None, max_retries=5, retry_delay=3)
    final_html = enity_response.text+entity_history.text
    if keyword in str(final_html):
        save_html_file(folder_name=folder_name, keyword=keyword, html_content=final_html)
        DbService().update_the_record_10(table_name, column_name, status_column,  keyword)

local_path = f'./{folder_name}/'
s3_path = f"s3://{AWS['bucket']}/DATA/{AWS['source']}/{AWS['folder']}/"
move_files(local_path, s3_path)

