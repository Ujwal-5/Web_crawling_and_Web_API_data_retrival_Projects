from selenium import webdriver
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from MySQLdb import _mysql
import random






options = ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.headless=False


driver = Chrome(options=options, version_main=120)
# driver.get('https://esos.nv.gov/EntitySearch/OnlineEntitySearch')
url = 'https://esos.nv.gov/EntitySearch/OnlineEntitySearch'
hostname = url.split('//')[1].split('/')[0]
print("Hostname being accessed:", hostname)

# Navigate to the URL
time.sleep(10)
driver.get(url)
wait = WebDriverWait(driver,30)


name = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="col-sm-3 col-md-3 col-lg-3"]/input[@class="form-control"]')))
name.send_keys('aaaa')

advanced_type = wait.until(EC.element_to_be_clickable((By.XPATH, '//select[@id="entityType"]')))
advanced_type.click()
type_option = wait.until(EC.element_to_be_clickable((By.XPATH,'//select[@id="entityType"]/option[@value="0"]')))
type_option.click()

status = wait.until(EC.element_to_be_clickable((By.XPATH, '//select[@id="entityStatus"]')))
driver.execute_script("arguments[0].click();", status)
status_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//select[@id="entityStatus"]/option[@value="0"]')))
status_option.click()


search_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="btnSearch"]')))
driver.execute_script("arguments[0].click();", search_button)

cookies = driver.get_cookies()
cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
print(cookie_string)

db=_mysql.connect("localhost","root","","crawler_db")
insert_query = f'''INSERT INTO NEVADAS_COOKIES (COOKIES) VALUES ('{cookie_string}')'''
print(insert_query)

db.query("set names utf8;")
db.query('SET NAMES utf8;')
db.query('SET CHARACTER SET utf8;')
db.query('SET character_set_connection=utf8;')
db.query(insert_query)


return_to_search = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@class="button loading"]')))
driver.execute_script("arguments[0].click();", return_to_search)

time.sleep(random.uniform(1,8))

driver.close()
driver.quit()
