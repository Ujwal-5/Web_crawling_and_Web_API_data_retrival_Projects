from glob import glob
import os
import shutil
import json
import time
import requests
import typing
import numpy as np
import cv2
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from mltu.inferenceModel import OnnxInferenceModel
from mltu.utils.text_utils import ctc_decoder

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("start-maximized")
# chrome_options.add_argument("--window-size=1020,900")
# chrome_options.add_argument('--dns-prefetch-disable')
# # chrome_options.add_argumFent("--headless")
# chrome_options.headless = False

options = ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.headless = True

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
    newMovelocation = "/home/oem/Desktop/SA/" + new_filename
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
conf = open('saudi.json')
# returns JSON object as 
# a dictionary
conFile = json.load(conf)
print('Hi')
driver = Chrome(options=options, version_main=major_version, use_subprocess=True)
print('Hello')
driver.maximize_window()
while 1:
    r = requests.get('http://34.240.143.117/Procedure/PROCEDURE_SAUDI_CSV.php?action=GET')
    keyworddata = r.json()
    print(keyworddata)

    ##cityVal = "الرياض"
    cityVal = keyworddata['url'];
    # print(cityVal)
    # cityVal = '4030501757'
    max_retries = 9
    retry_count = 0
    while retry_count < max_retries:
        try:
            driver.get("https://mc.gov.sa/ar/eservices/Pages/Commercial-data.aspx")
            time.sleep(5)
            # driver.find_element('id', 'advancedsearch').click()
            # time.sleep(5)
            imagexpath = driver.find_element(By.XPATH, '//img[@class="LBD_CaptchaImage"]')
            imagexpath.screenshot('foo.png');
            content = driver.page_source
            cookies_from_selenium = driver.get_cookies()

            cookies_for_requests = {cookie['name']: cookie['value'] for cookie in cookies_from_selenium}

            print('COKKIES value')
            print(cookies_for_requests)
            model = ImageToWordModel(model_path="model.onnx", char_list='fHjskV3241XOKtbxPcJh7e9doNqr6izn5puawvyl8gMmY')
            image = cv2.imread("foo.png")
            captchValue = model.predict(image)
            # imagexpath.screenshot('images/'+captchValue+'.png');

            # captchUrl.click()
            # print("//select[@class='ctrWidth ddlCRCity select2-hidden-accessible']/option[@value=" + cityVal + "]")
            # selectoption = driver.find_element(By.XPATH, "//select[@class='ctrWidth ddlCRCity select2-hidden-accessible']")
            # select = Select(selectoption)
            # cityVal = "الرياض"  # The value you want to select
            # select.select_by_value(cityVal)

            inputBoxCaptcha = driver.find_element(By.XPATH,
                                                  '//input[@name="ctl00$ctl73$g_7ccc91c8_7990_4f83_84c1_72d098d9838d$ctl00$CaptchaCodeTextBox"]').send_keys(
                captchValue)

            inputBoxCaptcha = driver.find_element(By.XPATH,
                                                  '//input[@name="ctl00$ctl73$g_7ccc91c8_7990_4f83_84c1_72d098d9838d$ctl00$txtCRName"]').send_keys(
                cityVal)

            time.sleep(3)
            inputBoxCaptcha = driver.find_element(By.XPATH, '//input[@type="submit"]').click()

            time.sleep(10)
            checkVal='مدة المنشأة'
            if checkVal in driver.page_source:
                content = driver.page_source
                f = open("html2/" + cityVal + ".html", "w",encoding='utf-8')
                print("CAPTCHA SUCCESS")
                f.write(content)
                f.close()
                requests.get('http://54.246.35.195/DEV2.0/Configrator/monitor.php?Browser='+conFile['Browser']+'&Service='+conFile['Service']+'&Machine_Name='+conFile['Machine_Name'])
                print("Heat")
                requests.get('http://34.240.143.117/Procedure/PROCEDURE_SAUDI_CSV.php?action=UPDATE&ID='+cityVal)
                break;
            else:
                continue;
        except TimeoutException:
            print("page page Timeout exception occurred. Retrying...")
            retry_count += 1
            continue;
        except NoSuchElementException:
            print("exception handled from main page")
            retry_count += 1
            continue;
