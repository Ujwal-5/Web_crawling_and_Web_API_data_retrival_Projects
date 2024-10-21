from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import json
import time
import random
from math import ceil
import mysql.connector
from mysql.connector import Error
import datetime
import os
from win32com.client import Dispatch
import traceback
import requests
import json
import subprocess
import psutil
from settings import MYSQL

def kill_chrome_process(driver):
    try:
        chrome_pid = driver.service.process.pid
        for process in psutil.process_iter():
            try:
                if process.pid == chrome_pid:
                    process.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except Exception as e:
        print(f"Error while killing Chrome process: {e}")

conf = open("xsmu.json") 
conFile = json.load(conf)  


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

class DbService:
    connection = None
    connection_mappings = None

    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=MYSQL['url'],
                user=MYSQL['username'],
                passwd=MYSQL['password'],
                database=MYSQL['schema'],
                port=MYSQL['port']
            )

            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    def close(self):
        # self.connection_mappings.close()
        self.connection.close()

    def get_crawling_numbers_counts(self,source):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * from crawling_numbers WHERE source_id = (SELECT id from sources WHERE code = '%s') AND status='UPDATE' "%source)
        result = cursor.fetchall()
        if cursor.rowcount > 0:
            return result
        return False

    def get_a_record_for_update(self,crawlType):
        cursor = self.connection.cursor()
        output = ''
        result_args = cursor.callproc("XSMUCBRD_uniquekey_procedure", args=(crawlType, output))
        print(output)
        return result_args

    def update_the_record(self, upd_date, label, source):
        cursor = self.connection.cursor()
        query = "UPDATE crawlings SET `update_date`='%s',`status`='0',`priority`=0 WHERE source_id = (SELECT id from sources WHERE code = '%s') AND label like '%s'"%(upd_date,source,label)
        print(query)
        cursor.execute(query)
        self.connection.commit()
        if cursor.rowcount > 0:
            return cursor.rowcount
        return False


# def processLog(log):
#     log = json.loads(log["message"])["message"]
#     if ("Network.response" in log["method"] and "params" in log.keys()):
#         headers = log["params"]["response"]
#         body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': log["params"]["requestId"]})
#         print(json.dumps(body, indent=4, sort_keys=True))
#         return log["params"]


def processLog(log):
    log = json.loads(log["message"])["message"]
    # print(log)
    if ("Network.responseReceived" in log["method"] and "params" in log.keys()):
        body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': log["params"]["requestId"]})
        return body
    else:
        return None


def getUserAgent(major_version):
    # print(user_agent)
    # return user_agent
    return f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{major_version}.0.0.0 Safari/537.36"


while True:
    current_directory = os.getcwd()
    reportsPath = f"{current_directory}/Reports/"
    if not os.path.exists(reportsPath):
        os.makedirs(reportsPath)
    print(f"Reports path: {reportsPath}")

    artDb = DbService()

    crawlNum = artDb.get_crawling_numbers_counts('XSMUCBRD')
    print(crawlNum)

    if crawlNum[0][3] <= 0 and crawlNum[1][3] <= 0:
        print("crawling_nums 0 for all types, closing crawler...")
        artDb.close()
        break

    print("Getting User Agent...")
    user_agent = getUserAgent(major_version)
    print(user_agent)
    print("Setting Capabilities...")
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {'performance': "ALL"}
    
    # CHROME_DRIVER_PATH = f"{current_directory}/chromedriver"
    # uc.TARGET_VERSION = 117
    
    
    chrome_options = uc.options.ChromeOptions()

    chrome_options.add_argument("--headless=new")
    # chrome_options.headless = False
    chrome_options.add_argument('--dns-prefetch-disable')
    chrome_options.add_argument(f'--user-agent={user_agent}')
    print("Starting Driver...")
    driver = uc.Chrome(options=chrome_options, use_subprocess=True, desired_capabilities=capabilities, version_main=major_version)
    print("Driver Started")
    driver.maximize_window()
    print("url: https://onlinesearch.mns.mu/")
    driver.get('https://onlinesearch.mns.mu/')
    wait = WebDriverWait(driver, 120)
    # exit()

    for crawling_nums in crawlNum:
        print(crawling_nums)
        print(f"Crawling type : {crawling_nums[2]}")
        print(f"crawling limit : {crawling_nums[3]}")


        crawlingLimit = crawling_nums[3]
        while crawlingLimit > 0:
            upd_recs = artDb.get_a_record_for_update(crawling_nums[2])
            fileNumber = (upd_recs[1].split("_"))[1]
            print(f"Record to be crawled: {fileNumber}  >> {upd_recs[1]}")

            todays_date = datetime.datetime.now().strftime("%Y-%m-%d")
            crawlingLimit -= 1
            try:
                requests.get('http://54.246.35.195/DEV2.0/Configrator/monitor.php?Browser='+conFile['Browser']+'&Service='+conFile['Service']+'&Machine_Name='+conFile['Machine_Name'])    
            except: 
                pass
            # response = driver.page_source
            # print(response)
            # forOtherBusiness = WebDriverWait(driver, 50).until(EC.presence_of_element_located((by=By.XPATH, value="//button[contains(@class,'search-other-business-btn')]")))
            # driver.execute_script("arguments[0].click();", forOtherBusiness)
            print("Setting search criteria...")
            clearSearchTxt = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//button[@type='button' and contains(@class,'clear-btn')]")))
            driver.execute_script("arguments[0].click();", clearSearchTxt)
            time.sleep(random.randint(1, 3))
            radioCheck = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@type='radio' and @formcontrolname='companySearchCriteria' and @id='fileNo']")))
            driver.execute_script("arguments[0].click();", radioCheck)
            time.sleep(random.randint(3, 5))
            print("Setting value search box...")
            driver.find_element(by=By.XPATH, value="//input[@type='text' and @formcontrolname='companyBusinessName' and @id='company-partnership-text-field']").send_keys(fileNumber)
            time.sleep(random.randint(1, 3))
            print("Submitting request...")
            submit = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]')))
            driver.execute_script("arguments[0].click();", submit)
            time.sleep(random.randint(3, 5))
            firstFileNo = None
            try:
                firstFileNo = driver.find_element(By.XPATH, '//tr[@class="ng-star-inserted"]/td[3]')
                print(firstFileNo.text)
            except:
                time.sleep(random.randint(1, 3))
                submit = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]')))
                driver.execute_script("arguments[0].click();", submit)
            time.sleep(random.randint(3, 5))
            print("Got the response checking logs for specific request...")
            logs = driver.get_log('performance')
            # print(logs)
            firstResponseList = ''
            if logs is not None:
                for log in logs:
                    log_2 = log['message']
                    # print(type(log_2))
                    if log_2.find("https://onlinesearch.mns.mu/onlinesearch/company") > 0 and log_2.find("requestId") > 0:
                        print("Found the desired response..")
                        # print(log_2)
                        log_2_json_object = json.loads(log_2)
                        # print(log_2_json_object)
                        # print(log_2_json_object['message']['method'])
                        # print(log_2_json_object['message']['params']['requestId'])
                        try:
                            requestId = log_2_json_object['message']['params']['requestId']
                            networkResponses = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
                            firstResponseList = json.loads(networkResponses['body'])
                            # print(firstResponseList)
                            if "totalElements" in firstResponseList:
                                print("Total no. of elements: %s" % firstResponseList['totalElements'])
                                break
                        except: 
                            continue
            print(firstResponseList)
            totalEntities = 0
            totalPages = 0
            perPageEntityCount = None
            if "totalElements" in firstResponseList:
                # WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class,"mat-form-field-flex")]')))
                # try:
                #     clickOption = driver.find_element(By.XPATH, '//div[contains(@class,"mat-form-field-flex")]')
                #     driver.execute_script("arguments[0].click();", clickOption)
                #     time.sleep(random.randint(3, 7))
                #     WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//mat-option[@role="option" and @id="mat-option-2"]')))
                #     clickOptionSelect = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//mat-option[@role="option" and @id="mat-option-2"]')))
                #     driver.execute_script("arguments[0].click();", clickOptionSelect)
                #     time.sleep(random.randint(5, 8))
                # except:
                #     print("Page Size Element Click Exception!")
                try:
                    print("Getting entity count on per page...")
                    perPageEntityCount = driver.find_element(By.XPATH, '//div[contains(@class,"mat-select-value")]/descendant::span[contains(@class,"mat-select-min-line")]')
                    print(perPageEntityCount.text)
                except:
                    print("Unable to get the count")
                try:
                    totalEntities = int(firstResponseList['totalElements'])
                    totalPages = ceil(totalEntities / int(perPageEntityCount.text))
                except:
                    totalPages = 0
            print("Total no. of pages: %s" % totalPages)
            if totalPages > 0:
                for page in range(1, int(totalPages)+1):
                    entityPerPage = int(perPageEntityCount.text)
                    if page == totalPages:
                        entityPerPage = int(totalEntities % int(perPageEntityCount.text))
                        if entityPerPage == 0:
                            entityPerPage = int(perPageEntityCount.text)
                    print(f"Total entities in this page is %d" % entityPerPage)
                    for entity in range(1, entityPerPage+1):
                        print("Page no. %s and entity no. %s" % (page, entity))
                    # if entity < 10:
                        #     continue
                        time.sleep(random.randint(1, 3))
                        try:
                            view = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, f"//tr[@class='ng-star-inserted'][{str(entity)}]/td[8]/div/fa-icon[@title='View']")))
                            time.sleep(random.randint(1, 3))
                            driver.execute_script("arguments[0].click();", view)
                            WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="dialog-close-button"]')))
                        except Exception as error:
                            print("Encountered an Exception!")
                            print(f"An exception occurred:{str(error)}")
                            print("Retrying one more time...")
                            time.sleep(random.randint(1, 5))
                            view = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, f"//tr[@class='ng-star-inserted'][{str(entity)}]/td[8]/div/fa-icon[@title='View']")))
                            driver.execute_script("arguments[0].click();", view)
                        time.sleep(random.randint(5, 7))
                        log_e = driver.get_log('performance')
                        for log in log_e:
                            # print(log)
                            log_3 = log['message']
                            if log_3.find("https://onlinesearch.mns.mu/onlinesearch/company/view") > 0 and log_3.find("requestId") > 0:
                                # print(log_3)
                                log_json_object = json.loads(log_3)
                                # print(log_json_object)
                                # print(log_json_object['message']['method'])
                                # print(log_json_object['message']['params']['requestId'])
                                try:
                                    requestId = log_json_object['message']['params']['requestId']
                                    networkResponses = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
                                    entityResponse = json.loads(networkResponses['body'])
                                    print(entityResponse)
                                except:
                                    print("JSONDecodeError: 296 line")
                                    continue

                                if "organisationInfo" in entityResponse:
                                    if "companyDetails" in entityResponse["organisationInfo"]:
                                        print("Got response for orgNo: %s and orgFileNo: %s ." % (entityResponse['organisationInfo']['companyDetails']['orgNo'], entityResponse['organisationInfo']['companyDetails']['orgFileNo']))
                                        fileName = str(entityResponse['organisationInfo']['companyDetails']['orgNo']) + '_' + entityResponse['organisationInfo']['companyDetails']['orgFileNo'] + '.json'
                                        json_file_path = os.path.join(reportsPath, fileName)
                                        with open(json_file_path, "w") as file1:
                                            json.dump(entityResponse, file1)
                                            upd_check = artDb.update_the_record(todays_date, upd_recs[1], 'XSMUCBRD')
                                            print(f"Records updated: {upd_check}")
                                elif "partnershipDetails" in entityResponse:
                                    print("Got response for orgNo: %s and orgFileNo: %s ." % (entityResponse['partnershipDetails']['orgNo'], entityResponse['partnershipDetails']['orgFileNo']))
                                    fileName = str(entityResponse['partnershipDetails']['orgNo']) + '_' + entityResponse['partnershipDetails']['orgFileNo'] + '.json'
                                    json_file_path = os.path.join(reportsPath, fileName)
                                    with open(json_file_path, "w") as file1:
                                        json.dump(entityResponse, file1)
                                        upd_check = artDb.update_the_record(todays_date, upd_recs[1], 'XSMUCBRD')
                                        print(f"Records updated: {upd_check}")
                                try:
                                    time.sleep(random.randint(2, 5))
                                    clickBtn = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="dialog-close-button"]')))
                                    driver.execute_script("arguments[0].click();", clickBtn)
                                except Exception as error:
                                    print("Encountered an Exception on click!")
                                    print(f"An exception occurred:{str(error)}")
                                break
                        time.sleep(random.randint(1, 3))
                    try:
                        time.sleep(random.randint(3, 7))
                        nextPage = driver.find_element(By.XPATH, '//button[ contains(@class,"mat-paginator-navigation-next") and contains(@aria-label,"Next page")]')
                        driver.execute_script("arguments[0].click();", nextPage)
                        time.sleep(random.randint(1, 3))
                    except Exception as error:
                        if page == totalPages:
                            print("Last Page Reached or got some issues...!")
                        else:
                            print("Faced some errors while crawling through the page...!")
                        print(f"An exception occurred:{str(error)}")
    time.sleep(random.randint(2, 6))
    driver.close()
    try:
        artDb.close()
    except:
        pass
    break

time.sleep(random.randint(1, 3))
try:
    subprocess.run(["aws", "s3", "mv", "./Reports/", f"s3://prod_buk/DATA/XSMUCBRD/TODO/", "--recursive"], check=True)
except: pass
try:
    kill_chrome_process(driver)
    driver.close()
    driver.quit()
except: pass
exit()