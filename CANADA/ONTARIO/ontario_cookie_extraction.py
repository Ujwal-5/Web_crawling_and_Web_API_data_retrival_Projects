import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import os
import json
import random
import ast
import string
import psutil
from twocaptcha import TwoCaptcha
from MySQLdb import _mysql
from win32com.client import Dispatch
import requests
conf = open('ontario.json')
# returns JSON object as 
# a dictionary
conFile = json.load(conf)

def process_tab(driver, random_alphabet):
    try:
        db = _mysql.connect("localhost","root","","crawler_db")
        driver.get("https://www.appmybizaccount.gov.on.ca/onbis/master/entry.pub?applicationCode=onbis-master&businessService=registerItemSearch")

        time.sleep(5)
        html_source = driver.page_source

        if "I'm not a robot" in html_source:
            flag = True
            i = 0
            while flag:
                i += 1
                captcha_image = WebDriverWait(driver, 50).until(
                    EC.visibility_of_element_located((By.XPATH, "//img[@class='captcha-code']")))
                captcha_image.screenshot('captcha.png')
                api_key = os.getenv('APIKEY_2CAPTCHA', 'your_2captcha_key')
                solver = TwoCaptcha(api_key)
                result = solver.normal('captcha.png')
                os.remove('captcha.png')
                captcha_text = result['code'].replace(' ', '').upper()
                captcha_text = captcha_text.upper()
                print('Solved: ' + str(captcha_text))
                captcha_box = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, 'solution')))
                driver.execute_script("arguments[0].value = arguments[1]", captcha_box, captcha_text)
                submit = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[text()="I\'m not a robot"]')))
                driver.execute_script("arguments[0].click();", submit)
                try:
                    time.sleep(5)
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '//button[text()="I\'m not a robot"]')))
                    print('Retrying captcha.............')
                    continue
                except:
                    flag = False
                    print('Captcha solved successfully ............')

        wait = WebDriverWait(driver, 90)
        search_box = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='QueryString']")))
        driver.execute_script("arguments[0].value = arguments[1]", search_box, random_alphabet)
        search = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'appButtonPrimary')]")))
        driver.execute_script("arguments[0].click();", search)
        time.sleep(10)
        
        # Your existing code to handle cookies here
        cokie = driver.get_cookies()
        cookies = ast.literal_eval(str(cokie))
        order = ['WRTCorrelator', 'dtCookie', 'x-catalyst-session-global', 'x-catalyst-timezone', 'JSESSIONID',
                 'QueueITAccepted-SDFrts345E-V3_onbis']
        ordered_cookies = [next((cookie['value'] for cookie in cookies if cookie['name'] == name), '') for name in order]
        result = '; '.join([f"{name}={value}" for name, value in zip(order, ordered_cookies) if value])
        print(result)
        insert_query = '''INSERT IGNORE INTO crawler_db.Ontario_cookies  (Cookie, Status) VALUE ('%s', '%s'); ''' %(result, 0)  
        db.query("set names utf8;")
        db.query('SET NAMES utf8;')
        db.query('SET CHARACTER SET utf8;')
        db.query('SET character_set_connection=utf8;')
        db.query(insert_query)

        try:
            requests.get('http://3.254.232.204/DEV2.0/Configrator/monitor.php?Browser='+conFile['Browser']+'&Service='+conFile['Service']+'&Machine_Name='+conFile['Machine_Name'])
            print("Moniter Heat")
        except:pass
        db.close()
        return result
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        print("Finally")




def main():
    chrome_options = uc.options.ChromeOptions()
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument('--dns-prefetch-disable')
    userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    chrome_options.add_argument(f'user-agent={userAgent}')

    driver = None  # Initialize the driver variable outside the with statement
    cookie_list=[]
    try:
        with uc.Chrome(options=chrome_options, version_main=major_version, use_subprocess=True) as temp_driver:
            driver = temp_driver  # Assign the driver to the outer variable
            alphabet_list = [random.choice(string.ascii_lowercase) for _ in range(5)]  # Adjust the number of tabs as needed

            for alphabet in alphabet_list:
                cookie_list.append(process_tab(driver, alphabet))
        return cookie_list
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if driver:
            chrome_pid = driver.service.process.pid
            for process in psutil.process_iter():
                try:
                    if process.pid == chrome_pid:
                        process.terminate()
                        print("end.")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
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
cookies = main()
 





