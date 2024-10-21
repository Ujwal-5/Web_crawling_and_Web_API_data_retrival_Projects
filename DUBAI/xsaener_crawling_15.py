from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import typing
import re
import undetected_chromedriver as uc
import cv2
import numpy as np
from MySQLdb import _mysql
from lxml import html
from mltu.configs import BaseModelConfigs
from mltu.inferenceModel import OnnxInferenceModel
from mltu.utils.text_utils import ctc_decoder
# import boto3
# from botocore.config import Config
# from botocore.exceptions import ClientError
from io import BytesIO
import psutil
# import botocore
import os
from win32com.client import Dispatch
import traceback
import subprocess
from xsaener_moniter import hit_moniter_api

def get_version_via_com(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version

if __name__ == "__main__":
    paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
             r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
             r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe",
             r"C:\Users\Admin\AppData\Local\Google\Chrome\Application\chrome.exe",
             r"C:\Users\Lenovo\AppData\Local\Google\Chrome\Application\chrome.exe"]
    version = list(filter(None, [get_version_via_com(p) for p in paths]))[0]
    print(version)

major_version = int(version.split('.')[0])
print(major_version)
print("Script started")
hit_moniter_api('xsaener_moniter.json')
# class StorageService:
#     s3_client = None
#     session = None

#     def __init__(self):
        # Create your own session
        # self.session = boto3.session.Session()

        # config = botocore.client.Config(
        #     retries={
        #         'max_attempts': 5,
        #         'mode': 'standard',
        #     },
        #     connect_timeout=3600,
        # )
        # # Now we can create low-level clients or resource clients from our custom session
        # self.s3_client = self.session.client('s3', config=config)

# Function to get the file size in bytes
def is_non_empty_file(filepath):
    return os.path.isfile(filepath) and os.path.getsize(filepath) > 0

def move_html_files_to_s3():
    # try:
    #     # List all JSON files in the local folder
    #     html_files = [f for f in os.listdir(local_folder) if f.endswith('.html')]
    #     print("files moved to s3:", html_files)

    #     # Upload each JSON file to S3 using the existing client
    #     for html_file in html_files:
    #         local_path = os.path.join(local_folder, html_file)
    #         # print('local_path', local_path)
    #         s3_key = os.path.join(s3_folder, html_file) if s3_folder else html_file
    #         # print(s3_key)
    #         self.s3_client.upload_file(local_path, bucket_name, s3_key)
    #         os.remove(local_path)

    # except ClientError as e:
    #     traceback.print_stack()
    #     print(e)
    #     return False

    try:
        # List all files in the current directory
        for filename in os.listdir("./"):
            # Check if the file is an HTML file and size is greater than 0 KB
            if filename.endswith(".html") and is_non_empty_file(filename):
                # Move the file using AWS CLI
                subprocess.run(["aws", "s3", "mv", filename, f"s3://prod_buk/DATA/XSAENER/todo_priority/{filename}"], check=True)
    except Exception as e:
        print(f"Error occurred: {e}")
    # try:
    #     subprocess.run(["aws", "s3", "mv", "./", "s3://prod_buk/DATA/XSAENER/todo/", "--recursive", "--exclude", "*", "--include", "*.html"], check=True)
    # except: pass
    
    return True

    # def move_html_single_file_to_s3(self, local_folder, html_file, bucket_name, s3_folder=''):
    #     try:
    #         local_path1 = os.path.join(local_folder, html_file)
    #         # print('local_path', local_path)
    #         s3_key1 = os.path.join(s3_folder, html_file) if s3_folder else html_file
    #         # print(s3_key)
    #         self.s3_client.upload_file(local_path1, bucket_name, s3_key1)
    #         os.remove(local_path1)
    #         print(f"{html_file} moved to s3")


    #     except ClientError as e:
    #         traceback.print_stack()
    #         print(e)
    #         return False
        
    #     return True
# storage_service = StorageService()

local_folder = os.getcwd()
bucket_name = 'prod_buk' 
# s3_folder = 'DATA/' + 'XSAENER' + '/todo/'

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


html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Details</title>
</head>
<body>
    <table border="1">
        <tr>
            <th>Field</th>
            <th>Value</th>
        </tr>
        <tr>
            <td>Expiry date</td>
            <td>{EXP_DATE}</td>
        </tr>
        <tr>
            <td>BL Status English</td>
            <td>{BL_STATUS}</td>
        </tr>
        <tr>
            <td>Emirate English</td>
            <td>{EM_ENG}</td>
        </tr>
        <tr>
            <td>BN EN</td>
            <td>{BN_EN}</td>
        </tr>
        <tr>
            <td>BN AR</td>
            <td>{BN_AR}</td>
        </tr>
        <tr>
            <td># BL</td>
            <td>{BL}</td>
        </tr>
    </table>
</body>
</html>
"""


chrome_options = uc.options.ChromeOptions()
#chrome_options = uc.ChromeOptions()
chrome_options.add_argument('--disable-dev-shm-usage') 
chrome_options.add_argument("--headless=new")
chrome_options.headless = True
chrome_options.add_argument('--dns-prefetch-disable')
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

driver = uc.Chrome(options=chrome_options, version_main=major_version, use_subprocess=True)
driver.maximize_window()
driver.get("https://ner.economy.ae/Search_By_CBLS_No.aspx")
english = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='English']")))
driver.execute_script("arguments[0].click();", english)
db=_mysql.connect("localhost","root","","crawler_db")
ct = 1

keywords = ['10866858','10866992', '10867077', '10867136','10871397','10871441','10871511','10871559','10871398','10868873','10868900','10868939','10869039','10869053','10870486','10874415','10875161','10875194']
try:
    loop = 0
    while loop<=20:
        loop+=1
        id_list = []
        keyword_list = []
        print(len(driver.window_handles))
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            flag = True
            # while flag:
            #     try:
            #         db.query("CALL PROCEDURE_URL_XSAENER(@p0,@p1);")
            #         db.query('SELECT @p0 AS `ID`,@p1 AS `KEYWORD`') 
            #         r=db.store_result()
            #         results=r.fetch_row()
            #         id = results[0][0].decode()
            #         keyword = results[0][1].decode()
            #         id_list.append(id)
            #         keyword_list.append(keyword)
            #         print('ID :', id, 'KEYWORD :', keyword)
            #         # keyword = 10003136
            #         flag = False
            #     except Exception as e: 
            #         print('Empty keyword / Deadlock issue', e)
            #         continue  
            keyword = keywords.pop()
            keyword_list.append(keyword)

            cbls_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'ctl00_MainContent_View_ucSearch_By_CBLS_No_cbpBreadCrumbOverAll_BAs_txtCBLSNo')))
            driver.execute_script("arguments[0].value = arguments[1]", cbls_box, keyword)
            flag = True
            i =0
            while flag: 
                i += 1
                captcha_image = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.ID, "ctl00_MainContent_View_ucSearch_By_CBLS_No_cbpBreadCrumbOverAll_BAs_ctlCaptcha_IMGD")))
                c_image = captcha_image.screenshot_as_png
                with open('screenshot.png', 'wb') as f:
                    f.write(c_image)
                    
                count = 0
                while count <= 3:
                    try:
                        image_array = np.array(bytearray(c_image), dtype=np.uint8)
                        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                        configs = BaseModelConfigs.load("configs.yaml")
                        model = ImageToWordModel(model_path="model.onnx", char_list=configs.vocab)
                        captcha_text = model.predict(image)
                        print('Solved: ' + str(captcha_text))
                        break
                    except Exception as e:
                        print(e)
                        count += 1
                        continue
                captcha_box = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'ctl00_MainContent_View_ucSearch_By_CBLS_No_cbpBreadCrumbOverAll_BAs_ctlCaptcha_TB_I')))
                driver.execute_script("arguments[0].value = arguments[1]", captcha_box, captcha_text)
                submit = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'ctl00_MainContent_View_ucSearch_By_CBLS_No_cbpBreadCrumbOverAll_BAs_btnSearchButton')))
                driver.execute_script("arguments[0].click();", submit)
                try: 
                    WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.ID,"ctl00_MainContent_View_ucSearch_By_CBLS_No_cbpBreadCrumbOverAll_BAs_lblIncorrectCodeMessage")))
                    continue
                except: 
                    print('break')
                    break
        # driver.switch_to.window(driver.window_handles[0])
        time.sleep(5)
        handle_count = 0
        # driver.implicitly_wait(60)
        print(driver.window_handles)
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            print(handle)
            # id_v  = id_list[handle_count]
            keyword_v  = keyword_list[handle_count]
            handle_count+=1
            output_page = driver.page_source
            if 'BL Status English' in output_page and 'BL #' in output_page:
                name_list = []
                value_list = []
                tatal_rows = 0
                active_row = 0
                with_detail = 0
                no_detail = 0
                f_page = 0
                try:
                    # time.sleep(5)
                    l1_page = driver.find_element(By.XPATH,"(//td[@class='dxpPageNumber'])[last()]").text
                    l_page = int(l1_page)
                except:
                    l_page = 0
                

                while f_page <= l_page:
                    f_page += 1
                    rows = driver.find_elements(By.XPATH, "//tr[contains(@id, 'ctl00_MainContent_View_ucSearch_By_CBLS_No_cbpBreadCrumbOverAll_BAs_GeneralSearchGridView_DXDataRow')]")
                    tatal_rows+=len(rows)

                    for current_row in range(len(rows)):
                        row = driver.find_element(By.XPATH, f"//tr[contains(@id, 'ctl00_MainContent_View_ucSearch_By_CBLS_No_cbpBreadCrumbOverAll_BAs_GeneralSearchGridView_DXDataRow{current_row}')]")
                        row_content = row.get_attribute('outerHTML') 
                        doc = html.fromstring(row_content)
                        BL_XPATH = f"//tr[@id='ctl00_MainContent_View_ucSearch_By_CBLS_No_cbpBreadCrumbOverAll_BAs_GeneralSearchGridView_DXDataRow{current_row}']/td[1]"
                        BN_AR_XPATH =  f"//tr[@id='ctl00_MainContent_View_ucSearch_By_CBLS_No_cbpBreadCrumbOverAll_BAs_GeneralSearchGridView_DXDataRow{current_row}']/td[2]"
                        BN_EN_XPATH =  f"//tr[@id='ctl00_MainContent_View_ucSearch_By_CBLS_No_cbpBreadCrumbOverAll_BAs_GeneralSearchGridView_DXDataRow{current_row}']/td[3]"
                        EM_ENG_XPATH =  f"//tr[@id='ctl00_MainContent_View_ucSearch_By_CBLS_No_cbpBreadCrumbOverAll_BAs_GeneralSearchGridView_DXDataRow{current_row}']/td[4]"
                        BL_STATUS_XPATH =  f"//tr[@id='ctl00_MainContent_View_ucSearch_By_CBLS_No_cbpBreadCrumbOverAll_BAs_GeneralSearchGridView_DXDataRow{current_row}']/td[6]"
                        EXP_DATE_XPATH = f"//tr[@id='ctl00_MainContent_View_ucSearch_By_CBLS_No_cbpBreadCrumbOverAll_BAs_GeneralSearchGridView_DXDataRow{current_row}']/td[8]"
                        # Define the XPaths
                        xpaths = {
                            'BL': str(BL_XPATH),
                            'BN_AR': str(BN_AR_XPATH),
                            'BN_EN': str(BN_EN_XPATH),
                            'EM_ENG': str(EM_ENG_XPATH),
                            'BL_STATUS': str(BL_STATUS_XPATH),
                            'EXP_DATE': str(EXP_DATE_XPATH)
                        }
                        # Fetch information using the XPaths
                        information = {}

                        for key, xpath in xpaths.items():
                            elements = doc.xpath(xpath)
                            if elements:
                                information[key] = elements[0].text.strip()
                            else:
                                information[key] = None
                        # Print the fetched information
                        for key, value in information.items():
                            print(f"{key}: {value}")
                        formatted_html = html_template.format(**information)
                        bn_en = information['BN_EN']
                        bn_ar = information['BN_AR']
                        
                        # Write the formatted HTML to a new file
                        nme=''
                        if bn_en!='':
                            nme=re.sub(r'[^a-zA-Z0-9]+', '-', bn_en)
                            file_name = f'XSAENER_{keyword_v}_{nme}.html'
                            # search_name = f"SELECT ID FROM URL_XSAENER_HISTORY WHERE FILE_NAME = '{file_name}'"
                            # db.query(search_name)
                            # r_n=db.store_result()
                            # results_n=r_n.fetch_row(5)
                            # if len(results_n) == 0:						
                                # with open(file_name, 'w', encoding='utf-8') as f:
                                #     f.write(formatted_html)
                            formatted_html_response = formatted_html
                            # else: 
                            #     while True:
                            #         try:
                            #             update_query = '''UPDATE TEMP_URL_XSAENER SET STATUS = 5 WHERE `KEYWORD` = %s ''' %(keyword_v) 
                            #             print(update_query)
                            #             db.query(update_query)
                            #             break
                            #         except:
                            #             continue
                            #     continue
                                        
                        elif bn_ar!='':
                            nme=bn_ar.replace(' ', '-')
                            file_name = f'XSAENER_{keyword_v}_{nme}.html'
                            # search_name = f"SELECT ID FROM URL_XSAENER_HISTORY WHERE FILE_NAME = '{file_name}'"
                            # db.query(search_name)
                            # r_n=db.store_result()
                            # results_n=r_n.fetch_row(5)
                            # if len(results_n) == 0:
                            formatted_html_response = formatted_html
                        #     else:
                        #         while True:
                        #             try:
                        #                 update_query = '''UPDATE TEMP_URL_XSAENER SET STATUS = 5 WHERE `KEYWORD` = %s ''' %(keyword_v) 
                        #                 print(update_query)
                        #                 db.query(update_query)
                        #                 break
                        #             except:
                        #                 continue
                        #         continue
                        # else:
                        #     print("No savable name")
                        #     continue
                        
                        xpath = "//a[contains(@class, 'aspNetDisabled')]"
                        element = doc.xpath(xpath)
                        if element:
                            print("Element with class 'aspNetDisabled' is present.")
                            no_detail +=1  
                            with open(file_name, 'w', encoding='utf-8') as file:
                                file.write(formatted_html_response)
                            time.sleep(3)
                
                            # response = move_html_files_to_s3()
                            # if response:
                            #     print("File uploaded successfully.")
                            # else:                                
                            #     print("File upload failed.")
                            # insert_query = '''INSERT INTO URL_XSAENER_HISTORY (`ID`, `CBLS_NO`, `FILE_NAME`, `ACTIVE_PAGENO`,`TOTAL_PAGENO`, `ACTIVE_ROWS`, `TOTAL_ROWS`, `NO_DETAILPAGE`, `DETAILPAGE`,`NO_DATA`) VALUES (%s, %s, '%s',%s,%s,%s,%s,%s,%s,%s) ''' %(id_v, keyword_v,  file_name, f_page, l_page, active_row,tatal_rows, no_detail,with_detail, 0) 
                            # print(insert_query)
                            # db.query("set names utf8;")
                            # db.query('SET NAMES utf8;')
                            # db.query('SET CHARACTER SET utf8;')
                            # db.query('SET character_set_connection=utf8;')
                            # db.query(insert_query)
                        else:
                            print("Element with class 'aspNetDisabled' is not present.")
                            with_detail+=1
                            detail = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, f"ctl00_MainContent_View_ucSearch_By_CBLS_No_cbpBreadCrumbOverAll_BAs_GeneralSearchGridView_cell{current_row}_25_Select")))
                            driver.execute_script("arguments[0].click();", detail)
                            popup = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "ctl00_MainContent_View_ucSearch_By_CBLS_No_popupBL_Detail_PWC-1")))
                            WebDriverWait(driver, 30).until(EC.visibility_of(popup))
                            popup_html = popup.get_attribute("innerHTML")
                            close = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID,"ctl00_MainContent_View_ucSearch_By_CBLS_No_popupBL_Detail_HCB-1Img")))
                            driver.execute_script("arguments[0].click();", close)
                            html_response = formatted_html_response+popup_html
                            with open(file_name, 'w', encoding='utf-8') as file:
                                file.write(str(html_response))
                            time.sleep(3)
                            # response = move_html_files_to_s3()

                            # if response:
                            #     print("File uploaded successfully.")
                            # else:
                            #     print("File upload failed.")
                            # insert_query = '''INSERT INTO URL_XSAENER_HISTORY (`ID`, `CBLS_NO`, `FILE_NAME`, `ACTIVE_PAGENO`,`TOTAL_PAGENO`, `ACTIVE_ROWS`, `TOTAL_ROWS`, `NO_DETAILPAGE`, `DETAILPAGE`,`NO_DATA`) VALUES (%s,%s,'%s',%s,%s,%s,%s,%s,%s,%s) ''' %(id_v, keyword_v, file_name, f_page, l_page, active_row,tatal_rows, no_detail,with_detail, 0) 
                            # print(insert_query)
                            # db.query("set names utf8;")
                            # db.query('SET NAMES utf8;')
                            # db.query('SET CHARACTER SET utf8;')
                            # db.query('SET character_set_connection=utf8;')
                            # db.query(insert_query)
                    current_row+=1
                    active_row+=current_row
                
                    if l_page!=0:
                        next_page = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//td[@class='dxpButton' and contains(@onclick, 'PBN')]/img[@alt='التالي']")))
                        driver.execute_script("arguments[0].click();", next_page)
                        f_page+=1
                        time.sleep(10)
                    # while True:
                    #     try:
                    #         update_query = '''UPDATE TEMP_URL_XSAENER SET STATUS = 10 WHERE `KEYWORD` = %s ''' %(keyword_v) 
                    #         print(update_query)
                    #         db.query(update_query)
                    #         break
                    #     except:continue
                            
            else:
                print('skip')
                # insert_query = '''INSERT INTO URL_XSAENER_HISTORY (`ID`, `CBLS_NO`, `FILE_NAME`, `ACTIVE_PAGENO`,`TOTAL_PAGENO`, `ACTIVE_ROWS`, `TOTAL_ROWS`, `NO_DETAILPAGE`, `DETAILPAGE`,`NO_DATA`) VALUES (%s,%s,'%s',%s,%s,%s,%s,%s,%s,%s) ''' %(id_v, keyword_v, 'NA', 0, 0, 0, 0, 0, 0, 1) 
                # print(insert_query)
                # db.query("set names utf8;")
                # db.query('SET NAMES utf8;')
                # db.query('SET CHARACTER SET utf8;')
                # db.query('SET character_set_connection=utf8;')
                # db.query(insert_query)
                # while True:
                #     try:
                #         update_query = '''UPDATE TEMP_URL_XSAENER SET STATUS = 5 WHERE `KEYWORD` = %s ''' %(keyword_v) 
                #         print(update_query)
                #         db.query(update_query)
                #         break
                #     except:continue
            
    try:
        driver.quit()
    except:pass
    try:
        db.close()
    except:pass
    
except Exception as e:
    print(traceback.print_exc())

# finally:
#     response = move_html_files_to_s3()
#     if response:
#         print("File uploaded successfully.")
#     else:
#         print("File upload failed.")
   
# for process in psutil.process_iter():
#     if process.name() == "chrome" or process.name() == "undetected_chromedriver":
#        process.kill()




