import requests
from database import DbService
from s3_move import move_files
from moniter import hit_moniter_api
from folder import create_folder
from custom_request import make_request_with_retry
from save_file import save_xml_file
from settings import AWS, MYSQL
from bs4 import BeautifulSoup
from data_extract import exract_data_using_xpath

folder_name = 'xml'
create_folder(folder_name=folder_name)

local_path = f'./{folder_name}/'
s3_path = f"s3://{AWS['bucket']}/DATA/{AWS['source']}/{AWS['folder']}/"
move_files(local_path, s3_path)

#Update table
table_name = MYSQL['table']
procedure_name = MYSQL['procedure']
procedure_parameter = MYSQL['procedure_parameter']
column_name = 'NIF'
status_column = 'STATUS'
hit_moniter_api('nif_moniter.json')

for _ in range(50):
    print('Script Started!')
    keyword = DbService().get_a_record(procedure_name, parameter=procedure_parameter)
    session = requests.Session()
    home_response = make_request_with_retry(url = "https://portaldocontribuinte.minfin.gov.ao/consultar-headNifId-do-contribuinte", session=session, method='get', headers=None, data=None, max_retries=5, retry_delay=3)
    soup = BeautifulSoup(home_response.text, 'html.parser')
    javax_viewstate = soup.find('input', {'name': 'javax.faces.ViewState'})
    event_state_value = javax_viewstate.get('value', '')
    # print(event_state_value)
    payload = {
        'javax.faces.partial.ajax': 'true',
        'javax.faces.source': 'j_id_2x:j_id_34',
        'javax.faces.partial.execute': 'j_id_2x',
        'javax.faces.partial.render': 'showpanelNIF',
        'j_id_2x:j_id_34': 'j_id_2x:j_id_34',
        'j_id_2x:txtNIFNumber': keyword,
        'j_id_2x_SUBMIT': '1',
        'javax.faces.ViewState':event_state_value
    }
    result_response = make_request_with_retry(url="https://portaldocontribuinte.minfin.gov.ao/consultar-headNifId-do-contribuinte", session=session, method='post', headers=None, data=payload, max_retries=5, retry_delay=3)
    nif_xpath = "//div[@id='showpanelNIF_content']//label[@id='taxPayerNidId']/text()"
    name_xpath = "//div[@id='showpanelNIF_content']//div[@class='form-group'][2]//label[@class='control-label text-left']/text()"
    if 'Resultado da Consulta' in result_response.text:  
        numeroNif = exract_data_using_xpath(response=result_response.text, xpath=nif_xpath)      
        nomeContribuinte = exract_data_using_xpath(response=result_response.text, xpath=name_xpath)  
        if numeroNif == None and nomeContribuinte==None:
            DbService().update_the_record(status =10, table=table_name, column=column_name, status_column=status_column,  keyword=keyword, isvalid=1, numeroNif=numeroNif, nomeContribuinte = nomeContribuinte)
            save_xml_file(folder_name=folder_name, keyword=keyword, xml_content=result_response.text)
        else:
            print("No data")
            DbService().update_the_record(status =10, table=table_name, column=column_name, status_column=status_column,  keyword=keyword, isvalid=0, numeroNif='NA', nomeContribuinte = 'NA')
    else:
        print("No data")
        DbService().update_the_record(status =10, table=table_name, column=column_name, status_column=status_column,  keyword=keyword, isvalid=0, numeroNif='NA', nomeContribuinte = 'NA')


move_files(local_path, s3_path)

