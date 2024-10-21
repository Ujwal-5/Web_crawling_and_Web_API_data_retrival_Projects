from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import traceback
import json
import tkinter as tk
import datetime
import sys
from database import DbService
from driver_config import DriverConf
from new_purchase import new_tab_purchase
from enter_captcha import manual_captcha_popup
from loguru import logger
from datetime import datetime

# Define the log file format with date
log_file_format = "logs_{time:YYYY-MM-DD}.log"

# Add a new log file with rotation based on date
logger.add(log_file_format, rotation="00:00", retention="1 day", level="INFO")

# Log your messages
driver_conf = DriverConf()
driver = driver_conf.load_page(url = 'https://www.e-services.cr.gov.hk/ICRIS3EP/system/home.do')
wait = WebDriverWait(driver, 180)
datbase_service = DbService()
driverconf = DriverConf()
try:
    popup = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="close ant-btn"]')))
    driver.execute_script("arguments[0].click();", popup)
except:
    print('No popup')

time.sleep(5)
user_id = WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH, '//input[@id="userId"]')))
# driver.execute_script("arguments[0].value = arguments[1]", user_id, 'hkoffice6')
user_id.send_keys('hkoffice6')
time.sleep(2)
password = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="password"]')))
# driver.execute_script("arguments[0].value = arguments[1]", password, 'Art000%000')
password.send_keys('Art000%000')
time.sleep(2)
login = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
driver.execute_script("arguments[0].click();", login)
logger.info('logged in')

try:
    popup_login_warning = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-modal-confirm-btns"]/button[@class="ant-btn ant-btn-primary"]')))
    driver.execute_script("arguments[0].click();", popup_login_warning)
    time.sleep(2)
except :
    print('No concurrent login warning')
    pass


cart = wait.until(EC.element_to_be_clickable((By.XPATH, '''//i[@class="icn cart"]''')))
driver.execute_script("arguments[0].click();", cart)
time.sleep(2)
cart_check = wait.until(EC.element_to_be_clickable((By.XPATH, '''//li[@class="iconBG icon-cart"]/a[contains(., 'Check Out Shopping Cart')]''')))
driver.execute_script("arguments[0].click();", cart_check)

captcha = manual_captcha_popup()

print('captcha', captcha)
captcha_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="captchaCode"]')))
captcha_field.send_keys(str(captcha))
time.sleep(2)

search_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="ant-checkbox"]/input[@value ="1"]/following-sibling::span')))
driver.execute_script("arguments[0].click();", search_checkbox)
time.sleep(2)

search_submit = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]/span[contains(text(), "Accept & Submit")]')))
driver.execute_script("arguments[0].click();", search_submit)
time.sleep(5)
logger.info('Solved the captcha')
session_id = driver.get_cookie('JSESSIONID')

createdat = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
session = session_id['value']
datbase_service.update_the_cookie(session, createdat) 
logger.info(f'Updated the cookie in the table :{session}')

while True:
    state, theid, brn =  datbase_service.validate_purchase()
    print('STATE :',state, 'THEID :',theid, 'BRN: ', brn)
    if state:
        logger.info('We have a order!!!!!')
        driver, order_number, remaining_balance, pay_status = new_tab_purchase(EC, By, wait, DriverConf, time, driver,brn, logger)
        print(order_number, remaining_balance, pay_status)
        datbase_service.update_the_status(order_number)
    time.sleep(60)