import lxml.html
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
local_path = f'./{folder_name}/'
s3_path = f"s3://{AWS['bucket']}/DATA/{AWS['source']}/{AWS['folder']}/"
move_files(local_path, s3_path)
#Update table
table_name = MYSQL['table']
procedure_name = MYSQL['procedure']
procedure_parameter = MYSQL['procedure_parameter']
column_name = 'entityID'
status_column = 'STATUS'


for _ in range(50):
    print('Script Started!')
    hit_moniter_api('wisconsin_crawl_moniter.json')
    time.sleep(random.uniform(3, 6))
    entityID = DbService().get_entityID_record(procedure_name=procedure_name, parameter=procedure_parameter)
    entity_entityID, hash_entityID = entityID.split('_')
    result_response = make_request_with_retry(url=f'https://www.wdfi.org/apps/CorpSearch/Details.aspx?entityID={entity_entityID}&hash={hash_entityID}', session=requests, method='get', headers=None, data=None, max_retries=5, retry_delay=3)
    # print(result_response.text)
    if entity_entityID in result_response.text:
        html_tree = lxml.html.fromstring(result_response.text)
        file_number = html_tree.xpath("//div[dl/dt[text()='File Number']]/dl/dd/text()")
        save_html_file(folder_name=folder_name, keyword=entity_entityID, html_content=result_response.text)
        DbService().update_the_record(status =10, table=table_name, column=column_name, status_column=status_column,  keyword=entityID)
    else:
        print("No data or error")
        DbService().update_the_record(status =5, table=table_name, column=column_name, status_column=status_column,  keyword=entityID)


move_files(local_path, s3_path)
