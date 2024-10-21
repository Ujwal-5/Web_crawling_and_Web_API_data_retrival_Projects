import requests
import json
from twocaptcha import TwoCaptcha
import os
import MySQLdb
from MySQLdb import _mysql
import sys
import sys
import time
import random
from retrying import retry
import subprocess
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from io import BytesIO
import botocore
import traceback

class StorageService:
    s3_client = None
    session = None

    def __init__(self):
        # Create your own session
        self.session = boto3.session.Session()

        config = botocore.client.Config(
            retries={
                'max_attempts': 5,
                'mode': 'standard',
            },
            connect_timeout=3600,
        )
        # Now we can create low-level clients or resource clients from our custom session
        self.s3_client = self.session.client('s3', config=config)
    
    def move_json_files_to_s3(self, local_folder, bucket_name, s3_folder=''):
        try:
            # List all JSON files in the local folder
            json_files = [f for f in os.listdir(local_folder) if f.endswith('.json')]
            print(json_files)

            # Upload each JSON file to S3 using the existing client
            for json_file in json_files:
                local_path = os.path.join(local_folder, json_file)
                # print('local_path', local_path)
                s3_key = os.path.join(s3_folder, json_file) if s3_folder else json_file
                # print(s3_key)
                self.s3_client.upload_file(local_path, bucket_name, s3_key)
                os.remove(local_path)


        except ClientError as e:
            traceback.print_stack()
            print(e)
            return False
        
        return True

# Example usage
local_folder = os.getcwd()
bucket_name = 'dev_buk'
s3_folder = 'DATA/' + 'AONIF' + '/json/'  # Optional: The desired folder structure in your S3 bucket

db = _mysql.connect('localhost', 'root', '', 'crawler_db')

storage_service = StorageService()
@retry(wait_fixed=10000, stop_max_attempt_number=10)
def send_post_request(url, data, headers):
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        response_data = response.json()
        return response_data
    except Exception as e:
        print(f"Request failed: {e}")
        raise			
        
@retry(wait_fixed=10000, stop_max_attempt_number=10)
def captcha_solve():
    try:
        api_key = os.getenv('APIKEY_2CAPTCHA', 'your_2captcha_key')
        solver = TwoCaptcha(api_key)
        result = solver.recaptcha(sitekey='6LfDAy4UAAAAAMjT7SItakjmnJFfeLUfzT8hMto8',
	                      url='https://agt.minfin.gov.ao/servico-comum/api/publico/comum/PortalAGT/consultar-nif',
	                      version='v2')
        return result
    except Exception as e:
        print(f"Request failed: {e}")
        raise

def crawl(temp_no):
    # try:
    print(temp_no)
    s = requests.Session()
    result = captcha_solve()
    url = "https://agt.minfin.gov.ao/servico-comum/api/publico/comum/PortalAGT/consultar-nif"
    data = {
        "ivNuContribuinte": temp_no,
        "reCapCaptcha": result['code']
    }

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        # "Cookie": "_ga=GA1.2.1078841459.1690557543; _gid=GA1.2.325912999.1690869740; _gat_AGT=1; _ga_PJX172EP=GS1.2.1690883038.5.1.1690883902.60.0.0",
        "Host": "agt.minfin.gov.ao",
        "Origin": "https://agt.minfin.gobreakv.ao",
        "Portal": "AGT",
        "Referer": "https://agt.minfin.gov.ao/PortalAGT/",
        "Sec-Ch-Ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Linux"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }
    response = send_post_request(url, data, headers)

        
    try:
        if response["data"] and not isinstance(response["data"], dict) and response["data"][0]["numeroNif"] and response["data"][0]["nomeContribuinte"]:
            print("valid Json")
            binaryData = json.dumps(response).encode("utf-8")
            file_name = f"{temp_no}.json"
            # response_s3 = storage_service.save_file_to_backup(binaryData, file_name)
            with open(f"{temp_no}.json", "w", encoding='utf-8') as file:
                json.dump(response, file, indent=2)
            time.sleep(3)
            response_s3 = storage_service.move_json_files_to_s3(local_folder, bucket_name, s3_folder)
            if response_s3:
                print("File uploaded successfully.")
            else:
                print("File upload failed.")
            # print(f"file moved {temp_no}.json")

            for _ in range(5):
                try:
                    update_query = '''UPDATE URL_AONIF 
                  SET STATUS = 20, `IS_VALID` = 1, `numeroNif` = '%s', `nomeContribuinte` = '%s' 
                  WHERE `NIF` = %s''' % (response["data"][0]["numeroNif"], response["data"][0]["nomeContribuinte"], temp_no)
 
                    print(update_query)
                    db.query(update_query)
                    break
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e) 
        pass
    return False

for _ in range(5):
    try:
        select_query = ('''SELECT NIF FROM URL_AONIF WHERE `STATUS`=10 AND `IS_VALID` =1 LIMIT 50''')
        db.query(select_query)
        r=db.store_result()
        data=r.fetch_row(50)
        print(data)
        for _ in range(5):
            try:
                update_query = '''UPDATE URL_AONIF SET STATUS=19 WHERE NIF IN ({})'''.format(','.join([str(nif[0].decode()) for nif in data]))
                db.query(update_query)
                print(update_query)
                break
            except Exception as e:
                print(e)
        for en_nif in data:
            crawl(en_nif[0].decode())
            time.sleep(random.uniform(2, 5))
        break

    except Exception as e:
        print(e)







