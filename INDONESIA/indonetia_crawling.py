import time
from selenium.webdriver.common.by import By
import requests
from twocaptcha import TwoCaptcha
import urllib.parse
import shutil
import os
from MySQLdb import _mysql
import undetected_chromedriver as uc
from win32com.client import Dispatch
import traceback
import sys
import requests
import json
import psutil
import random
from ml_captch_solver import captcha_ml_solver

def hit_moniter_api(file_name):
    conf = open(file_name) 
    conFile = json.load(conf)   
    try:
        requests.get('http://3.254.232.204/DEV2.0/Configrator/monitor.php?Browser='+conFile['Browser']+'&Service='+conFile['Service']+'&Machine_Name='+conFile['Machine_Name'])    
    except: pass

hit_moniter_api('indo.json')

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

try:
    # Open the browser using Selenium
    chrome_options = uc.options.ChromeOptions()
    #chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--window-size=1020,900")
    chrome_options.add_argument('--dns-prefetch-disable')
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-background-networking')
    chrome_options.add_argument('--disable-background-timer-throttling')
    chrome_options.add_argument('--disable-plugins')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--enable-low-end-device-mode')
    chrome_options.add_argument('--disable-notifications')
    # chrome_options.add_argument('--headless-new')
    chrome_options.headless = False

    driver = uc.Chrome(options=chrome_options, version_main=major_version, use_subprocess=True)
    db=_mysql.connect("localhost","root","","crawler_db")
    # driver = webdriver.Chrome()  # You need to have Chrome WebDriver installed
    driver.get("https://ereg.pajak.go.id/ceknpwp")

    # Wait for the page to load
    time.sleep(5)  # Adjust the time as needed based on your internet speed

    # Get cookies
    cookies = driver.get_cookies()
    print(cookies)
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])


    for _ in range(50):
        time.sleep(random.uniform(3, 6))
        for _ in range(5):
            try:
                db.query("CALL PROCEDURE_KEYWORD_4_Indonesia(@p);")
                db.query('SELECT @p AS `KEYWORD`') 
                r=db.store_result()
                results=r.fetch_row()
                keyword = results[0][0].decode()
                print('KEYWORD :', keyword)
                break
            except Exception as e: 
                print('Empty keyword / Deadlock issue', e)
                # print(traceback.print_exc())
                continue  
        else:
            sys.exit()

        if len(keyword) > 6:
            # Iterate and split the keyword, adding each substring to a list
            keyword_parts = [keyword[:i+1] for i in range(6, len(keyword))]

        else:
            keyword_parts = [keyword]

        # Print each part
        print(keyword_parts)
        for part_key in keyword_parts:
            print(part_key)
            element = driver.find_element(By.XPATH, "//img[@id='captcha']")
            element_data = element.get_attribute("src")
            # print(element_data)

            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'en-US,en;q=0.9,en-IN;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                # 'Cookie': 'TS00000000076=08eef1bd54ab280077b4da0c2e7ac80f3d0f4226b89bf09195276c85478b171e48ecf7813cec20f35ee5c41c2f92427008eb9542b309d00056b2c1d22c582cc4bd2d9ed2e9de716369dcb31b508b504cfc758a5dc65b639ea9219ee8b8678ab0daa2cbf861b5d41593d509a7bc3d5b4c391d9f289c4f2c534d52a119432536ea92e1df5a92516dad91c2374916032c0c0298655237ce3aa0edb18b8ba638fc04b78fc2ac8aae9f05d5cc251975fe5291c6dc4575adc60c5025e9e4af956603eef757fa60feac41e75db005eb458cb23232ca504d014e768f305bfa1123d27848b0c1cf86293989d78b11d85435d5bf4cece3976ab909da232c753cceb5db9301f60904a8b4709a63; TSPD_101_DID=08eef1bd54ab280077b4da0c2e7ac80f3d0f4226b89bf09195276c85478b171e48ecf7813cec20f35ee5c41c2f92427008eb9542b3063800823b7c48834859809ca2cf2ae06d73abea27cfbd37a5929ad632a0655aea1e9a1c6439395ff6ddb6ad0c6ea2966223b0d105d057700f131c; EREGSID=Z6CMMldYhN8VOnDSfPuBxdNw; TS017f6355=01099e3f0df8cadbdb8d6c410431a870d2cb68089f60dc8a16627ec247e3178ea70c4bf4e0a2e707183fdb9dc5011e5d8b4dcc9f96d8b99b178d5579d2d69b32f99e95a3e0; TSd30f64ea027=08eef1bd54ab2000cfe3edf8fec7019a8c1b5fa8a5fb298337a0d850cbccacba7a0f61d92d8f7f8d089a84e253113000ba0d28db9f48ae9d54f69c1951025d24cef1e6040d0e7740db51e2feba135d72958a444887cec2ca8cecbd905a1d7700',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
                'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }

            responseImage = session.get(
                    element_data,
                    headers=headers,
                    verify=False
                )
            # print(responseImage)
            # print(responseImage.content)
            # Save the image
            with open('captcha.png', 'wb') as f:
                f.write(responseImage.content)

            captcha_value =captcha_ml_solver()
            # keyword = 'AAAA'
            # solver = TwoCaptcha('your_2captcha_key')
            # result = solver.normal('captcha_image.png')
            # print(result)

            headers = {
                'Accept': '',
                'Accept-Language': '',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                # 'Cookie': 'TS00000000076=08eef1bd54ab2800e9f0180803c957dbd5d49f126ebc7d25c2f0b15d41f215ddb78879800052945f963632543da7f53b08831d99f709d0003b90c4f4184e68edfd2959098ec93a44518f0db656db0e0cab694d5325a202305ac3b29d521944fa680b6ca944b58e5f84abce66374a1152ea5c2c8ca8da71713d38aa19361ef38d859669f397cd2092a4d063a596cd0099a82ee38546efe8e391cbeb731d0f299054e0c66ba28a68ced5efb82b151d93ae81e3fd83e2c7295eecfcc7cbccc9a655b4e96e59b4a5446c41463fc9c6a425df16c5e3320bcdb19fa7d8b6377fa30bdeb993167ee8454ff16bf059130c644a81dec0044e06287ff22af02baef5c618dcb64808896738cc10; TSPD_101_DID=08eef1bd54ab2800e9f0180803c957dbd5d49f126ebc7d25c2f0b15d41f215ddb78879800052945f963632543da7f53b08831d99f7063800cb30596618663ab70dc418ce8a3f149f51b5a7f7f984eef8cc8a09864f3cda772c233e4f47f0a1c7264ef55809f91fd62b1f3ae7a828f332; EREGSID=zzzwqoyIr-M3YrqH6JI4xRoO; TS017f6355=01099e3f0dc8e1ff087dc48fc109ed68de51328855b67de04d9d1fbda3d1fc6faa8481567122a55957abb596cb82222f9c1a9eeac3405e97d052657238e55b6f363b2829d0; TSd30f64ea027=08eef1bd54ab2000a4a9ed4c1c6200d9d3b75707cd2f1a6440a30a35afde594c3926b192ceb31f6908900c664711300066c728622da13035405e8e742d7a2a746b2d144e2105ac53b958e40bc595ebae3645dd4ed9e32843c1644009dd703905',
                'Origin': 'https://ereg.pajak.go.id',
                'Referer': 'https://ereg.pajak.go.id/ceknpwp',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
                'X-Requested-With': '',
                'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }
            #nama=Dunia+Virtual&noAkta=AHU-0028368.AH.01.01.Tahun+2022&captcha=u7zj
            data = {
                'nama': part_key,
                'noAkta': '',
                'captcha': captcha_value,
            }
            encoded_data = urllib.parse.urlencode(data, quote_via=urllib.parse.quote_plus)

            # print(encoded_data)
            response = session.post('https://ereg.pajak.go.id/ceknpwpbadan', headers=headers, data=encoded_data, verify= False)
            json_data = response.json()
            print(json_data)
            if json_data["s"]=="0":
                if os.path.exists('captcha.png'):
                    os.remove('captcha.png')
                    print(f"captcha_image.png has been deleted.")
                else:
                    print(f"captcha_image.png does not exist.")
                for _ in range(5):
                    try:
                        db.query(f'UPDATE TEMP_KEYWORDS_4_Indonesia SET FLAG = 5 WHERE KEYWORD = "{keyword}"')
                        print(f'UPDATE TEMP_KEYWORDS_4_Indonesia SET FLAG = 5 WHERE KEYWORD = "{keyword}"')
                        break
                    except:
                        print(traceback.print_exc())
                        pass

            elif json_data["s"]=="1":
                with open('json/'+str(part_key)+'.json', 'w') as f:
                    f.write(json.dumps(json_data))
                if os.path.exists('captcha.png'):
                    os.remove('captcha.png')
                    print(f"captcha_image.png has been deleted.")
                else:
                    print(f"captcha_image.png does not exist.")
                for _ in range(5):
                    try:
                        db.query(f'UPDATE TEMP_KEYWORDS_4_Indonesia SET FLAG = 10, KEYWORD_2 = "{part_key}", LENGHT = "{len(part_key)}" WHERE KEYWORD = "{keyword}"')
                        print(f'UPDATE TEMP_KEYWORDS_4_Indonesia SET FLAG = 10, KEYWORD_2 = "{part_key}", LENGHT = "{len(part_key)}" WHERE KEYWORD = "{keyword}"')
                        break
                    except:
                        print(traceback.print_exc())
                        pass
                    
                    
                values = [(record.get('nwp'), record.get('nm')) for record in json_data['d']]

                if len(values) > 500:
                    # Split the values into chunks of 500
                    chunks = [values[i:i+500] for i in range(0, len(values), 500)]

                    for chunk in chunks:
                        placeholder_list = [f"({v[0]}, {v[1]})" for v in chunk]  # Create placeholders with values
                        placeholders = ', '.join(placeholder_list)

                        # Construct the query with concatenated placeholders
                        insert_query = f"""INSERT IGNORE INTO Indonesia_DATA_Crawling (nwp, Name) VALUES {placeholders}"""

                        insert_query = insert_query % values  # Values still used for parameter injection
                        print(insert_query)

                        for _ in range(5):
                            try:
                                db.query(insert_query)
                                print(f"Inserted {len(chunk)} records successfully.")
                                break
                            except Exception as e:
                                # db.rollback()
                                print(f"Failed to insert records: {e}")
                                print(traceback.print_exc())
                else:
                    # Insert all values in a single query (similar to previous option)
                    placeholder_list = [f"('''{v[0]}''', '''{v[1]}''')" for v in values]
                    placeholders = ', '.join(placeholder_list)
                    insert_query = f"""INSERT IGNORE INTO Indonesia_DATA_Crawling (nwp, Name) VALUES {placeholders}"""
                    insert_query = insert_query % values

                    for _ in range(5):
                        try:
                            db.query(insert_query)
                            print(f"Inserted {len(values)} records successfully.")
                            break
                        except Exception as e:
                            # db.rollback()
                            print(f"Failed to insert records: {e}")
                            print(traceback.print_exc())
                        
            else:
                for _ in range(5):
                    try:
                        db.query(f'UPDATE TEMP_KEYWORDS_4_Indonesia SET FLAG = 5 WHERE KEYWORD = "{keyword}"')
                        print(f'UPDATE TEMP_KEYWORDS_4_Indonesia SET FLAG = 5 WHERE KEYWORD = "{keyword}"')
                        break
                    except:
                        print(traceback.print_exc())
                        pass

finally:
    print('closing the driver')
    try:
        db.close()
    except:
        print(traceback.print_exc())
        pass

    try:
        chrome_pid = driver.service.process.pid
        for process in psutil.process_iter():
            try:
                if process.pid == chrome_pid:
                    process.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                print(traceback.print_exc())
                pass
    except:
        pass
    try:
        driver.quit()
    except:
        print(traceback.print_exc())
        pass