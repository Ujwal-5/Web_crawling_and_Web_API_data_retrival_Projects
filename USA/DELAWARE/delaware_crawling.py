# from driver_config import DriverConf
# from lxml import html
from folder import create_folder
from settings import MYSQL, AWS
from database import DbService
# from bs4 import BeautifulSoup
import traceback
import random
from s3_move import move_files, configure_aws
from selenium.webdriver.common.keys import Keys
# from DrissionPage import ChromiumPage
import time
from DrissionPage import ChromiumOptions, ChromiumPage
import os,urllib,random,pydub,speech_recognition,time
from DrissionPage.common import Keys
import sys
# import psutil
import requests
import json
import sys
from moniter import hit_moniter_api


def store_data_s3(content, c_id):
    data = {
        'HTML': content,
        'NAME': c_id,
        'USER_ID': 'ujwal-py'
    }
    # print('data', data)
    json_data = json.dumps(data)

    try:
        print('API requests')
        url = 'http://18.201.184.118/xsusreg-delaware-data-configure_api/DEConfigureS3.php'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json_data, headers=headers)
        return(response)

    except requests.exceptions.RequestException as e:
        print('Error: ', e)

# Example usage


class RecaptchaSolver:
    def __init__(self, driver:ChromiumPage):
        self.driver = driver
    
    def solveCaptcha(self):
        iframe_inner = self.driver("@title=reCAPTCHA")
        time.sleep(0.1)
        
        # Click on the recaptcha
        iframe_inner('.rc-anchor-content',timeout=1).click()
        self.driver.wait.ele_displayed("xpath://iframe[contains(@title, 'recaptcha')]",timeout=3)

        # Sometimes just clicking on the recaptcha is enough to solve it
        if self.isSolved():
            return
        
        
        # Get the new iframe
        iframe = self.driver("xpath://iframe[contains(@title, 'recaptcha')]")
        print(iframe)
        # Click on the audio button
        try:
         iframe('#recaptcha-audio-button',timeout=5).click()
        except: 
            print(traceback.print_exc())
            iframe = self.driver("xpath://iframe[contains(@title, 'recaptcha')]")

        time.sleep(3)
        print(iframe)
        
        # Get the audio source
        src = iframe('#audio-source').attrs['src']
        print(src)
        print('hi')
        
        # Download the audio to the temp folder
        path_to_mp3 = os.path.normpath(os.path.join((os.getenv("TEMP") if os.name=="nt" else "/tmp/")+ str(random.randrange(1,1000))+".mp3"))
        path_to_wav = os.path.normpath(os.path.join((os.getenv("TEMP") if os.name=="nt" else "/tmp/")+ str(random.randrange(1,1000))+".wav"))
        print(path_to_mp3)
        print(path_to_wav)
        urllib.request.urlretrieve(src, path_to_mp3)

        # Convert mp3 to wav
        sound = pydub.AudioSegment.from_mp3(path_to_mp3)
        sound.export(path_to_wav, format="wav")
        sample_audio = speech_recognition.AudioFile(path_to_wav)
        r = speech_recognition.Recognizer()
        with sample_audio as source:
            audio = r.record(source)
        
        # Recognize the audio
        key = r.recognize_google(audio)
        print(key)
        if key == '':
            page.quit()
            sys.exit()

        
        # Input the key
        iframe('#audio-response').input(key.lower())
        time.sleep(0.1)
        
        # Submit the key
        iframe('#audio-response').input(Keys.ENTER)
        time.sleep(.4)

        # Check if the captcha is solved
        if self.isSolved():
            return
        else:
            raise Exception("Failed to solve the captcha")

    def isSolved(self):
        try:
            check_mark =  self.driver.ele(".recaptcha-checkbox-checkmark",timeout=3).attrs
            print(check_mark)
            return 'style' in check_mark 
        except:
            return False
        
co = ChromiumOptions()
# co.headless()  # 无头模式
# co.set_argument('--no-sandbox')
page = ChromiumPage(co)
recaptchaSolver = RecaptchaSolver(page)
# configure_aws(access_key_id = AWS['access_key'], secret_access_key = AWS['secret_key'], region = AWS['region_name'])

folder_name = 'html'
create_folder(folder_name=folder_name)
#Update table
table_name = MYSQL['table']
procedure_name = MYSQL['procedure']
procedure_parameter = MYSQL['procedure_parameter']
column_name = 'company_number'
status_column = 'STATUS'
no = 2
local_path = f'./{folder_name}/'
s3_path = f"s3://{AWS['bucket']}/DATA/{AWS['source']}/{AWS['folder']}/"
# move_files(local_path, s3_path)

# sys.exit()
# 访问网页 (Visit a webpage)
for _ in range(5):
    try:
        page.get("https://icis.corp.delaware.gov/eCorp/EntitySearch/NameSearch.aspx")
        for _ in range(30):
            hit_moniter_api('delaware_moniter.json')
            keyword =  DbService().get_a_record(procedure_name, parameter=procedure_parameter)
            time.sleep(random.uniform(0,3))
            page('#ctl00_ContentPlaceHolder1_frmFileNumber', timeout=30).input(keyword)
            time.sleep(random.uniform(0,3))
            # page('@type=password').input('Food@123')
            page('#ctl00_ContentPlaceHolder1_btnSubmit',timeout=30).click()
            time.sleep(random.uniform(0,3))
            for i in range(5):
                print(f'{i+1} try')
                page.wait.eles_loaded('#ctl00_ContentPlaceHolder1_btnSubmit')  # 等待 id 为 div1 的元素加载

                if 'ctl00_ContentPlaceHolder1_rptSearchResults_ctl00_lnkbtnEntityName' not in str(page.html):
                    t0 = time.time()
                    try:
                        recaptchaSolver.solveCaptcha()
                    except:
                        pass
                    time.sleep(random.uniform(0,3))
                    page('@type=submit').click()
                    print(f"Time to solve the captcha: {time.time()-t0:.2f} seconds")
                    time.sleep(random.uniform(0,3))
                    page('#ctl00_ContentPlaceHolder1_frmFileNumber', timeout=30).input(keyword)
                    time.sleep(random.uniform(0,3))
                    # page('@type=password').input('Food@123')
                    page('#ctl00_ContentPlaceHolder1_btnSubmit',timeout=30).click()
                
                elif 'No Records Found.' in str(page.html):
                    DbService().update_the_record(1, table_name, column_name, status_column, keyword)
            
                else:
                    print('success')
                    time.sleep(random.uniform(0,3))
                    page('#ctl00_ContentPlaceHolder1_rptSearchResults_ctl00_lnkbtnEntityName', timeout=30).click()
                    time.sleep(random.uniform(0,3))
                    page.wait.eles_loaded('#ctl00_ContentPlaceHolder1_btnReturn')
                    current_page = page.html
                    if 'Entity Details' in str(current_page) and keyword in str(current_page):
                        print('saving the file')
                        with open(f'html/DE-{keyword}.html', mode ='w', encoding='utf-8') as file:
                            file.write(page.html)
                        response = store_data_s3(current_page, keyword)
                        print(response.status_code)
                        if response.status_code ==200:
                            DbService().update_the_record(100, table_name, column_name, status_column, keyword)
                        # else:
                        #     DbService().update_the_record(, table_name, column_name, status_column, keyword)
                    page('#ctl00_ContentPlaceHolder1_btnReturn', timeout=30).click()
                    # move_files(local_path, s3_path)
                    time.sleep(random.uniform(5,15))
                    # sys.exit()
                    break
    except:
        print(traceback.print_exc())
        pass


# 502 Bad Gateway