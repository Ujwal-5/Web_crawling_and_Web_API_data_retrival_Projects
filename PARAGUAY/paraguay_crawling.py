from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from itertools import product
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from loguru import logger


log_file_format = "logs_{time:YYYY-MM-DD}.log"
logger.add(log_file_format, rotation="00:00", retention="1 day", level="INFO")

def generate_keywords():
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    keywords = [''.join(combination) for combination in product(letters, repeat=3)]
    return keywords

keywords = generate_keywords()
print(keywords)
cut_count = keywords.index('MCI')
keywords=keywords[cut_count:]
print(keywords)
logger.info(f'Total keywords {keywords}')

#create chromeoptions instance
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--no-sandbox")
# options.headless = False
options.add_argument('--disable-dev-shm-usage')

#provide location where chrome stores profiles
options.add_argument(r"--user-data-dir=C:\\Users\\sujwa\\AppData\\Local\\Google\\Chrome\\User Data")

#provide the profile name with which we want to open browser
options.add_argument(r'--profile-directory=Default') # Profile 1

#specify where your chrome driver present in your pc
driver = webdriver.Chrome(options=options)

#provide website url here
driver.get("https://ruc.com.py/index.php/inicio/login_with_google")
# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(., "Continue")]'))).click()


for i in keywords:
    logger.info(i)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//input[@type="text"]'))).send_keys(i)
    # time.sleep(2)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'btn_buscar'))).click()
    # time.sleep(2)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//input[@type="text"]'))).clear()
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '(//tbody[@style="display: table-row-group;"]/tr/td[contains(., "-")])[1]') or (By.XPATH, '//td[contains(., "Item no encontrado")]')))        # time.sleep(3)
        html = driver.page_source
        
        if 'Item no encontrado' not in str(html):
            with open(f'html/{i}.html', mode='w', encoding='utf-8') as file:
                file.write(html)
            logger.info(f'sucussfully saved file for : {i}')
       
        else:
            logger.info(f'No data found : {i}')

    except:
        try:
            html = driver.page_source
        
            if 'Item no encontrado' in str(html):
                logger.info(f'No data found : {i}')
            else:
                logger.info(f'something wrong : {i}')
                
        except:
            logger.info(f'error : {i}')            

#find element using its id
# print(driver.find_element("id","home").text)