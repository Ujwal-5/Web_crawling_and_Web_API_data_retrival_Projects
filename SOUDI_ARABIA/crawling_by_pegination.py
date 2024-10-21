from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from openpyxl import load_workbook
import lxml.etree as ET
import undetected_chromedriver as uc
from glob import glob
import os
import shutil
# import parallelTestModule
import multiprocessing as mp
from multiprocessing.sharedctypes import Value
import pytesseract
from bs4 import BeautifulSoup
import time
import random
import math
import xmltodict, json
import json
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import cv2
import pytesseract
from selenium.webdriver.common.by import By
import whisper
import speech_recognition as sr
from selenium.webdriver.support.ui import Select
from faster_whisper import WhisperModel


model_size = "base"
model = WhisperModel(model_size, device="cpu", compute_type="int8")
r = sr.Recognizer()
#model = whisper.load_model("base")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--window-size=1020,900")
chrome_options.add_argument('--dns-prefetch-disable')
chrome_options.add_argument("--headless")


def download_audio(url, output_path):
    # Send a GET request to download the file
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the content of the response (M4A file) to a local file
        with open(output_path, "wb") as file:
            file.write(response.content)
        print("✅ M4A file downloaded successfully.")
    else:
        print("❌ Failed to download the audio file.")


def get_last_filename_and_rename(save_folder, new_filename):
    files = glob(save_folder + '/*')
    max_file = max(files, key=os.path.getctime)
    filename = max_file.split("/")[-1]
    extension = filename.rsplit(".")[-1]
    print('NEw file=' + filename)
    print('extension file=' + extension)
    new_filename = new_filename + '.' + extension
    print('extension file=' + new_filename)
    new_path = max_file.replace(filename, new_filename)
    # print(new_path)
    os.rename(max_file, new_path)
    # print(new_path)
    # newMovelocation=new_path.replace('/Downloads/', '/Downloads/poland1/')
    # print(newMovelocation)
    newMovelocation = "C:/wamp64/www/SA" + new_filename
    shutil.move(new_path, newMovelocation)
    return new_path


def worldToNumber(stringVal):
    word_to_number = {
        'zero': 0,
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'ten': 10
    }

    # Input sentence containing words to convert
    input_sentence = stringVal.replace(' ', '').replace('.', '').replace("-", ',').lower()

    # Split the input sentence into words
    words = input_sentence.split(',')

    # Convert words using the dictionary
    converted_numbers = [str(word_to_number.get(word, word)) for word in words]

    # Join the converted numbers back into a sentence
    output_sentence = ''.join(converted_numbers)
    return output_sentence


def download_mp3_file(url, save_path, cookies):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        # 'Cookie': '_ga_4YR34K1HVZ=GS1.1.1691666106.3.1.1691667959.0.0.0; _ga=GA1.3.777771735.1690795281',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }
    print('get request')
    print(url)
    response = requests.get(url, cookies=cookies, headers=headers)

    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {url} to {save_path}")
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")


driver = uc.Chrome(options=chrome_options, use_subprocess=True)
driver.maximize_window()


r = requests.get('http://54.246.35.195/DEV2.0/Configrator/procedure_SA.php?action=GET')
keyworddata = r.json()
print(keyworddata)

##cityVal = "الرياض"
cityVal=keyworddata['url'];
print(cityVal)
max_retries = 9
retry_count = 0
while retry_count < max_retries:
    try:
        driver.get("https://mc.gov.sa/ar/eservices/Pages/Commercial-data.aspx")
        time.sleep(5)
        driver.find_element('id', 'advancedsearch').click()
        time.sleep(5)
        imagexpath = driver.find_element(By.XPATH, '//img[@class="LBD_CaptchaImage"]')
        imagexpath.screenshot('foo.png');
        content = driver.page_source
        f = open("abc1.html", "w", encoding="utf-8")
        f.write(content)
        f.close()
        # Speak the CAPTCHA code
        # captchUrl = driver.find_element(By.XPATH, '//a[@id="c__catalogs_masterpage_innerpage_ctl00_ctl73_g_7ccc91c8_7990_4f83_84c1_72d098d9838d_ctl00_examplecaptcha_SoundLink"]/a[1]/@href')
        captchUrl = driver.find_element(By.XPATH, '//a[@class="LBD_SoundLink"]').get_attribute('href')
        print(captchUrl)
        cookies_from_selenium = driver.get_cookies()

        cookies_for_requests = {cookie['name']: cookie['value'] for cookie in cookies_from_selenium}

        print('COKKIES value')
        print(cookies_for_requests)
        download_mp3_file(captchUrl, 'a2.wav', cookies_for_requests)

        # get_last_filename_and_rename("/home/oem/Downloads",'cap')
        #result = model.transcribe("a1.wav", fp16=False)
        #print(result["text"])
        #captchValue = worldToNumber(result["text"])
        #print('captcha value')
        #print(captchValue)
        segments, _ = model.transcribe("a2.wav", beam_size=5)
        result={}
        for segment in segments:
          result["text"] = segment.text
        captchValue = worldToNumber(result["text"])
        print(captchValue)
        # captchUrl.click()
        print("//select[@class='ctrWidth ddlCRCity select2-hidden-accessible']/option[@value=" + cityVal + "]")
        selectoption = driver.find_element(By.XPATH, "//select[@class='ctrWidth ddlCRCity select2-hidden-accessible']")
        select = Select(selectoption)
        # cityVal = "الرياض"  # The value you want to select
        select.select_by_value(cityVal)

        inputBoxCaptcha = driver.find_element(By.XPATH,
                                              '//input[@name="ctl00$ctl73$g_7ccc91c8_7990_4f83_84c1_72d098d9838d$ctl00$CaptchaCodeTextBox"]').send_keys(
            captchValue)

        time.sleep(3)
        inputBoxCaptcha = driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        time.sleep(20)
        content = driver.page_source
        f = open("html2/" + cityVal + "_1" + ".html", "w", encoding="utf-8")
        f.write(content)
        f.close()
        dataout = driver.find_element(By.XPATH, '//div[@id="pagingDivClient"]/a[1]')
        driver.execute_script("SearchByPaging(4); return false;", dataout)
        break;
    except TimeoutException:
        print("page page Timeout exception occurred. Retrying...")
        retry_count += 1
        continue;
    except NoSuchElementException:
        print("exception handled from main page")
        retry_count += 1
        continue;

conf = open('sa_2.json') 
conFile = json.load(conf)   
lo = int(keyworddata['activepage'])
while lo < 1991:
    lo = lo + 1
    max_retries = 9
    retry_count = 0
    while retry_count < max_retries:
        try:
            print(lo)
            dataout = driver.find_element(By.XPATH, '//div[@id="pagingDivClient"]/a[1]')
            time.sleep(5)
            driver.execute_script("SearchByPaging(" + str(lo) + "); return false;", dataout)
            time.sleep(5)
            content = driver.page_source
            f = open("html2/" + cityVal + "_" + str(lo) + ".html", "w", encoding="utf-8")
            f.write(content)
            f.close()
            requests.get('http://54.246.35.195/DEV2.0/Configrator/procedure_SA.php?action=UPDATE&id=' + keyworddata[
                    'id'] + "&ACTIVE_PAGE=" + str(lo))
            requests.get('http://54.246.35.195/DEV2.0/Configrator/monitor.php?Browser='+conFile['Browser']+'&Service='+conFile['Service']+'&Machine_Name='+conFile['Machine_Name'])        
            print("Action performed successfully.")
            break  # Break out of the loop on successful
        except TimeoutException:
            print("Timeout exception occurred. Retrying...")
        except NoSuchElementException:
            print("exception handled1")
            driver.find_element('id', 'advancedsearch').click()
            time.sleep(5)
            imagexpath = driver.find_element(By.XPATH, '//img[@class="LBD_CaptchaImage"]')
            imagexpath.screenshot('foo.png');
            content = driver.page_source
            f = open("abc1.html", "w")
            selectoption = driver.find_element(By.XPATH,
                                               "//select[@class='ctrWidth ddlCRCity select2-hidden-accessible']")
            select = Select(selectoption)
            select.select_by_value(cityVal)
            captchUrl = driver.find_element(By.XPATH, '//a[@class="LBD_SoundLink"]').get_attribute('href')
            print(captchUrl)
            cookies_from_selenium = driver.get_cookies()
            cookies_for_requests = {cookie['name']: cookie['value'] for cookie in cookies_from_selenium}
            print('COKKIES value')
            print(cookies_for_requests)
            download_mp3_file(captchUrl, 'b2.wav', cookies_for_requests)
            #result = model.transcribe("b1.wav")
            segments, _ = model.transcribe("b2.wav", beam_size=5)
            result={}
            for segment in segments:
              result["text"] = segment.text
            #print(result["text"])
            captchValue1 = worldToNumber(result["text"])
            #result = model.transcribe("b1.wav", fp16=False)
            #print(result["text"])
            #captchValue1 = worldToNumber(result["text"])
            #print('captcha value')
            print(captchValue1)
            inputBoxCaptcha = driver.find_element(By.XPATH,
                                                  '//input[@name="ctl00$ctl73$g_7ccc91c8_7990_4f83_84c1_72d098d9838d$ctl00$CaptchaCodeTextBox"]').send_keys(
                captchValue1)

            time.sleep(3)
            inputBoxCaptcha = driver.find_element(By.XPATH, '//input[@type="submit"]').click()
            # dataout = driver.find_element(By.XPATH, '//div[@id="pagingDivClient"]/a[1]')
            # time.sleep(5)
            # driver.execute_script("SearchByPaging(" + str(lo) + "); return false;", dataout)

        retry_count += 1

if retry_count == max_retries:
    print("Max retries reached. Action could not be performed.")
