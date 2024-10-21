import requests
import json
from IPython.display import display, Image, HTML
import re
import mysql.connector
from mysql.connector import Error
from lxml import html
import time
import os 
from PIL import Image as Img
from io import BytesIO
import shutil
from lxml import html
from mltu.configs import BaseModelConfigs
from mltu.inferenceModel import OnnxInferenceModel
from mltu.utils.text_utils import ctc_decoder
import cv2
import numpy as np
import typing
import random
import string
import pandas as pd

# api_key = os.getenv('APIKEY_2CAPTCHA', 'your_2captcha_key')
# solver = TwoCaptcha(api_key)
conf = open('xsinepfo.json') 
conFile = json.load(conf)  

while True:
    try:
        try:
            requests.get('http://54.246.35.195/DEV2.0/Configrator/monitor.php?Browser='+conFile['Browser']+'&Service='+conFile['Service']+'&Machine_Name='+conFile['Machine_Name'])    
        except: pass

        class ImageToWordModel(OnnxInferenceModel):
            def __init__(self, char_list: typing.Union[str, list], *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.char_list = char_list

            def predict(self, image: np.ndarray):
                image = cv2.resize(image, self.input_shape[:2][::-1])
                image_pred = np.expand_dims(image, axis=0).astype(np.float32)
                preds = self.model.run(None, {self.input_name: image_pred})[0]
                text = ctc_decoder(preds, self.char_list)[0]
                return text

        class DbService:
            connection = None
            connection_mappings = None

            def __init__(self):         

                try:
                    self.connection = mysql.connector.connect(
                        host='localhost',
                        user='root',
                        passwd='',
                        database='crawler_db',
                        port='3306'
                    )

                    print("Connection to MySQL DB successful")
                except Error as e:
                    print(f"The error '{e}' occurred")

            def close(self):
                # self.connection_mappings.close()
                self.connection.close()


            def get_a_record(self, max_retries=3, retry_delay=1):
                    cursor = self.connection.cursor()
                    try:
                        cursor.execute('CALL `PROCEDURE_XSINEPFO_V2`(@p0, @p1)')
                        cursor.execute("SELECT @p0 AS `id`, @p1 AS `keyword`;")
                        results = cursor.fetchall()
                        # Update the status to 9 for the selected rows
                        if results:
                            id = results[0][0]
                            keyword = results[0][1]
                            print('id', id, 'keyword', keyword)
                            # Commit the changes
                            self.connection.commit()
                            return id, keyword
                    except mysql.connector.Error as e:
                        print(f"An error occurred while executing the database query: {e}")
                        cursor.close()
                        if max_retries > 0:
                            print("Retrying in a moment...")
                            time.sleep(retry_delay)
                            return self.get_a_record(max_retries=max_retries-1, retry_delay=retry_delay)
                        else:
                            print("Maximum retries reached. Returning None.")
                            return None

            def update_the_record(self, keyword, max_retries=3, retry_delay=1):
                cursor = self.connection.cursor()
                try:
                    print(keyword)
                    update_query = f"UPDATE `KEYWORDS_XSINEPFO_V2` SET `FLAG` = 10 WHERE `KEYWORD` = '{keyword}'"
                    cursor.execute(update_query)
                    self.connection.commit()
                    cursor.close()
                    return False
                except mysql.connector.Error as e:
                    print(f"An error occurred while updating the record: {e}")
                    if cursor is not None:
                        cursor.close()
                    if max_retries > 0:
                        print("Retrying in a moment...")
                        time.sleep(retry_delay)
                        return self.update_the_record(keyword, max_retries=max_retries-1, retry_delay=retry_delay)
                    else:
                        print("Maximum retries reached. Returning False.")
                        return False
                    

        database_service = DbService()      
        # ----------------------------------------------------------------------------------------------------------------------------

        id, keyword  = database_service.get_a_record()
        print(keyword)
        response_home = requests.get('https://unifiedportal-epfo.epfindia.gov.in/publicPortal/no-auth/misReport/home/loadEstSearchHome')
        # Display the image

        # display(HTML(response_2.text))
        html_code = str(response_home.text)
        pattern_createCaptcha = r"/publicPortal/no-auth/captcha/createCaptcha\?_HDIV_STATE_=([^\'\s]+)"
        match_url = re.search(pattern_createCaptcha, html_code)

        if match_url:
            createCaptcha = match_url.group(1)
            createCaptcha_value = createCaptcha.rstrip('"')
            print("Target Value :", createCaptcha_value)
        else:
            print("Target value from URL not found.")
            
        headers_home = response_home.headers
        # Parse the Set-Cookie header to get JSESSIONID and SERVERID
        set_cookie_header = headers_home.get('Set-Cookie', '')
        cookie_parts = [part.strip() for part in set_cookie_header.split(',')]
        # Extract JSESSIONID and SERVERID
        jsessionid = None
        serverid = None
        for part in cookie_parts:
            if part.startswith('JSESSIONID='):
                jsessionid = part.split('=')[1].split(';')[0]
            elif part.startswith('SERVERID='):
                serverid = part.split('=')[1].split(';')[0]

        # Print the results
        print("JSESSIONID:", jsessionid)
        print("SERVERID:", serverid)

        url = f"https://unifiedportal-epfo.epfindia.gov.in/publicPortal/no-auth/captcha/createCaptcha?_HDIV_STATE_={createCaptcha_value}"

        payload = f"_HDIV_STATE_={createCaptcha_value}"
        headers = {
        'Cookie': f'JSESSIONID={jsessionid}; SERVERID={serverid}',
        'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        display(Image(response.content))
        captcha_name = random.choice(string.ascii_uppercase)

        with open(f'{captcha_name}.png', 'wb') as f:
            f.write(response.content)

        # ------------------------------------------------------------------------------------


        pattern_searchEstablishment = r"/publicPortal/no-auth/estSearch/searchEstablishment\?_HDIV_STATE_=([^\'\s]+)"
        match_searchEstablishment = re.search(pattern_searchEstablishment, html_code)

        if match_searchEstablishment:
            searchEstablishment = match_searchEstablishment.group(1)
            searchEstablishment_value = searchEstablishment.rstrip('"')
            print("Target SEARCH HDIV Value :", searchEstablishment_value)
        else:
            print("Target value from URL not found.")

        search_url = f"https://unifiedportal-epfo.epfindia.gov.in/publicPortal/no-auth/estSearch/searchEstablishment?_HDIV_STATE_={searchEstablishment_value}"
        print(search_url)
        count = 0
        while count <= 3:
            try:
                image = cv2.imread(f'{captcha_name}.png')
                model = ImageToWordModel(model_path="model.onnx", char_list="LRFACOW_QUYE3\u20756JDZSN8I+2V1TK4PMB07X59\xCDGH")
                captcha_text = model.predict(image)
                # captcha_text = 'MAGIC'
                print('Solved: ' + str(captcha_text))
                os.remove(f'{captcha_name}.png')
                break
            except Exception as e:
                print(e)
                count += 1
                continue


        # current_path = 'captcha.png'
        # destination_folder = 'Captcha/'
        # new_filename = f'{str(captcha_text)}.png'

        # destination_path = os.path.join(destination_folder, new_filename)
        # shutil.move(current_path, destination_path)

        search_payload = json.dumps({
        "EstName": keyword,
        "EstCode": "",
        "captcha": str(captcha_text)
        })

        print(search_payload)
        search_headers = {
        'Cookie': f'JSESSIONID={jsessionid}; SERVERID={serverid};',
        'Content-Type': 'application/json'
        }
        print(search_headers)
        response_search = requests.request("POST", search_url, headers=search_headers, data=search_payload)


        # display(HTML(response_search.text))
        # -----------------------------------------------------------------------------------------------------

        tree = html.fromstring(response_search.text)
        tr_elements = tree.xpath('//tr')

        # List to store extracted information
        data_list = []

        # Loop through each <tr> element
        for tr_element in tr_elements:
            # Use XPath to extract information from <td> elements within the current <tr>
            td_elements = tr_element.xpath('.//td[@style="text-align: left;"]/text()')

            # Extracted information
            establishment_code = td_elements[0].strip() if td_elements else ""
            company_name = td_elements[1].strip() if len(td_elements) > 1 else ""
            address_line = td_elements[2].strip() if len(td_elements) > 2 else ""
            city = td_elements[3].strip() if len(td_elements) > 3 else ""

            # Add the extracted information to the list
            data_list.append(f"{id}", f"{establishment_code}")

        print(data_list)
        df = pd.DataFrame({'Id': data_list})

        # Specify the CSV file name
        csv_filename = 'establishment_codes.csv'
        # Append the DataFrame to the CSV file (mode='a' for append)
        df.to_csv(csv_filename, mode='a', header=False, index=False)
        print(f'Data for  has been successfully appended to {csv_filename}')
        database_service.update_the_record(keyword)
    except: pass
