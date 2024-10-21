import json
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from io import BytesIO
from settings import AWS

def save_html_file(folder_name, keyword, html_content):
    with open(f'{folder_name}/{keyword}.html', mode = 'w', encoding='utf-8') as file:
        file.write(html_content)

def save_json_file(folder_name, keyword, json_content):
    with open(f'{folder_name}/{keyword}.json', mode ='w', encoding='utf-8') as file:
        json.dump(json_content, file, indent=4)
    

class save_file_s3():
    s3_client = None
    session = None   

    def __init__(self):
        self.session = boto3.Session()
        # self.session = boto3.Session(aws_access_key_id=AWS['access_key'],
        #                              aws_secret_access_key=AWS['secret_key'],
        #                              region_name= AWS['region_name'])

        config = Config(
            retries = {
                'max_attempts': 5,
                'mode': 'standard',
            },
            connect_timeout = 3600
        )
        self.s3_client = self.session.client('s3', config=config)

    def save_file_to_s3_backup(self, content, file_name):
        try:
            destination_path = 'DATA/' + AWS['source'] +'/'+AWS['folder']+'/' + file_name
            out_file = BytesIO(content)
            out_file.seek(0)
            response = self.s3_client.put_object(Body=out_file, Bucket=AWS['bucket'], Key=destination_path)
        except ClientError as e:
            return False
        return response