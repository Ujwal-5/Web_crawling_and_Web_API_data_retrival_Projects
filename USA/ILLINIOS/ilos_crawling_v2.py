from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import random
from MySQLdb import _mysql
from urllib.parse import urlencode
import traceback
import requests
import json
import subprocess
import psutil
from win32com.client import Dispatch
 

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
options = ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
# options.add_argument('--headless=new')
options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"')
options.headless = False

db=_mysql.connect("localhost","root","","crawler_db")

def get_file_number():
    for _ in range(10):
        try:
            db.query("CALL PROCEDURE_URL_FILES_ILSOS(@p,@p1);")
            db.query('SELECT @p AS `SR_NO`,@p1 AS `FILE_NUMBER`') 
            r=db.store_result()
            results=r.fetch_row()
            SR_NO = results[0][0].decode()
            FILE_NUMBER = results[0][1].decode()
            print('SR_NO :', SR_NO, 'FILE_NUMBER :', FILE_NUMBER)
            return FILE_NUMBER
            break
        except Exception as e: 
            print('Empty keyword / Deadlock issue', e)
            continue 

driver = Chrome(options=options, version_main=major_version)
driver.get('https://apps.ilsos.gov/businessentitysearch/')
wait = WebDriverWait(driver, 30)

MAX_RETRIES = 3

def click_with_retry(element):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            driver.execute_script("arguments[0].click();", element)
            # driver.execute_script("var ele = arguments[0];ele.addEventListener('click', function() {ele.setAttribute('automationTrack','true');});",element)
            # if element.get_attribute("automationTrack"):
            return True
            # else:
            #     retries += 1
            #     print(f"Click failed. Element not clickable. Retrying... ({retries}/{MAX_RETRIES})")
            #     time.sleep(random.uniform(1, 3))
        except Exception as e:
            retries += 1
            print(f"Click failed. Retrying... ({retries}/{MAX_RETRIES})")
            time.sleep(random.uniform(1, 3))
    
    return False

for _ in range(60):
    try:
        time.sleep(random.uniform(1, 4))
        File_number = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@value="f"]')))
        if not click_with_retry(File_number):
            print("Failed to click File_number. Skipping iteration.")
            continue

        FILE_NUMBER = get_file_number()
        time.sleep(random.uniform(1, 6))
        new_search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@id="searchValue"]')))
        new_search.send_keys(f'{FILE_NUMBER}')

        time.sleep(random.uniform(1, 6))
        submit = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Submit"]')))
        if not click_with_retry(submit):
            print("Failed to click Submit. Skipping iteration.")
            continue
        html_index = driver.page_source
        time.sleep(random.uniform(1, 6))
        Entity_name = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#getDetails"]')))
        if not click_with_retry(Entity_name):
            print("Failed to click Entity_name. Skipping iteration.")
            continue

        time.sleep(random.uniform(1, 6))
        html_content = driver.page_source
        full_html = html_index+html_content
        if 'Entity Information' in full_html and FILE_NUMBER in full_html:
            with open(f"html/{FILE_NUMBER}.html", "w", encoding="utf-8") as file:
                file.write(full_html)
            db.query(f'UPDATE `URL_ILSOS` SET STATUS = 10 WHERE FILE_NUMBER = {FILE_NUMBER}')
        driver.back()
    except Exception as e:
        print(traceback.format_exc())
        driver.get('https://apps.ilsos.gov/businessentitysearch/')
        pass