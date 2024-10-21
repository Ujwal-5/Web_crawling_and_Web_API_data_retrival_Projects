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
                host="localhost",
                user="root",
                passwd="",
                database="crawler_db",
                port="3306"
            )

            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    def close(self):
        self.connection_mappings.close()
        self.connection.close()

    def get_crawling_numbers_counts(self,source):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * from crawling_numbers WHERE source_id = (SELECT id from sources WHERE code = '%s') AND status='UPDATE' "%source)
        result = cursor.fetchall()
        if cursor.rowcount > 0:
            return result
        return False
   
    def get_a_record_for_update(self,source):
        cursor = self.connection.cursor()
        cursor.execute("SELECT label from crawlings WHERE source_id = (SELECT id from sources WHERE code = '%s') AND (DATEDIFF(CURRENT_DATE ,`update_date`)> 90 OR `update_date`='0000-00-00' ) AND label LIKE 'I________' ORDER BY `priority` DESC limit 1"%source)
        result = cursor.fetchall()
        if cursor.rowcount > 0:
            return result
        return False

    def update_the_record(self, upd_date, label, source):
        cursor = self.connection.cursor()
        query = "UPDATE crawlings SET `update_date`='%s',`status`='0' WHERE source_id = (SELECT id from sources WHERE code = '%s') AND label like '%s'"%(upd_date,source,label)
        # ,`priority`=0
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


def getUserAgent():
    user_agent = f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{major_version}.0.0.0 Safari/537.36"
    # print(user_agent)
    # return user_agent
    return f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{major_version}.0.0.0 Safari/537.36"


while True:
    current_directory = os.getcwd()
    reportsPath = f"{current_directory}/ReportsX/"
    if not os.path.exists(reportsPath):
        os.makedirs(reportsPath)
    print(f"Reports path: {reportsPath}")

    print("Getting User Agent...")
    user_agent = getUserAgent()
    print(user_agent)
    print("Setting Capabilities...")
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {'performance': "ALL"}
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

    artDb = DbService()

    crawlNum = artDb.get_crawling_numbers_counts('XSMUCBRDX')
    print(crawlNum)
    for crawling_nums in crawlNum:
        print(crawling_nums)
        print(f"Crawling type : {crawling_nums[2]}")
        print(f"crawling limit : {crawling_nums[3]}")

        crawlingLimit = crawling_nums[3]
        FOUND = 0
        while crawlingLimit > 0:
            upd_recs = artDb.get_a_record_for_update("XSMUCBRDX")
            print(upd_recs)
            fileNumber = upd_recs[0]
            print(f"Record to be crawled: {fileNumber}  >> {upd_recs[0]}")
            todays_date = datetime.datetime.now().strftime("%Y-%m-%d")
            crawlingLimit -= 1

            try:
                requests.get('http://54.246.35.195/DEV2.0/Configrator/monitor.php?Browser='+conFile['Browser']+'&Service='+conFile['Service']+'&Machine_Name='+conFile['Machine_Name'])    
            except: 
                pass
            # response = driver.page_source
            # print(response)
            if FOUND == 0:
                forOtherBusiness = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'search-other-business-btn')]")))
                driver.execute_script("arguments[0].click();", forOtherBusiness)
            print("Setting search criteria...")
            clearSearchTxt = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//button[@type='button' and contains(@class,'clear-btn')]")))
            driver.execute_script("arguments[0].click();", clearSearchTxt)
            time.sleep(random.randint(1, 3))
            radioCheck = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, "//input[@type='radio' and @formcontrolname='otherBusinessSearchCriteria' and @id='other-business-brn']")))
            driver.execute_script("arguments[0].click();", radioCheck)
            time.sleep(random.randint(3, 5))
            print("Setting value search box...")
            driver.find_element(by=By.XPATH, value="//input[@type='text' and @formcontrolname='otherBusinessName' and @id='other-business-text-field']").send_keys(fileNumber)
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
            # driver.close()
            # exit()
            firstResponseList = ''
            if logs is not None:
                for log in logs:
                    log_2 = log['message']
                    # print(type(log_2))
                    if log_2.find("https://onlinesearch.mns.mu/onlinesearch/business") > 0 and log_2.find("requestId") > 0:
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
                        except: 
                            continue
                        # print(firstResponseList)
                        if "totalElements" in firstResponseList:
                            print("Total no. of elements: %s" % firstResponseList['totalElements'])
                            break
            print(firstResponseList)
            totalEntities = 0
            totalPages = 0
            # driver.close()
            # exit()
            perPageEntityCount = 1
            busOrgNumber = ''
            if "totalElements" in firstResponseList:
                if  len(firstResponseList['results']) != 0:
                    busOrgNumber = firstResponseList['results'][0]['busOrgNumber']
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
                totalPages = 1
            print("Total no. of pages: %s" % totalPages)
            if totalPages > 0 and busOrgNumber != '':
                for page in range(1, int(totalPages)+1):
                    entityPerPage = int(perPageEntityCount)
                    if page == totalPages:
                        entityPerPage = int(totalEntities % int(perPageEntityCount))
                        if entityPerPage == 0:
                            entityPerPage = int(perPageEntityCount)
                    print(f"Total entities in this page is %d" % entityPerPage)
                    for entity in range(1, entityPerPage+1):
                        print("Page no. %s and entity no. %s" % (page, entity))
                    # if entity < 10:
                        #     continue
                        time.sleep(random.randint(1, 3))
                        try:
                            view = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, f"//tr[@class='ng-star-inserted'][{str(entity)}]/td[7]/div/fa-icon[@title='View']")))
                            time.sleep(random.randint(1, 3))
                            driver.execute_script("arguments[0].click();", view)
                            WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="dialog-close-button"]')))
                        except Exception as error:
                            print("Encountered an Exception!")
                            print(f"An exception occurred:{str(error)}")
                            print("Retrying one more time...")
                            time.sleep(random.randint(1, 5))
                            view = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, f"//tr[@class='ng-star-inserted'][{str(entity)}]/td[7]/div/fa-icon[@title='View']")))
                            driver.execute_script("arguments[0].click();", view)
                        time.sleep(random.randint(5, 7))
                        log_e = driver.get_log('performance')
                        for log in log_e:
                            # print(log)
                            log_3 = log['message']
                            if log_3.find("https://onlinesearch.mns.mu/onlinesearch/business/view") > 0 and log_3.find("requestId") > 0:
                                # print(log_3)
                                log_json_object = json.loads(log_3)
                                # print(log_json_object)
                                # print(log_json_object['message']['method'])
                                # print(log_json_object['message']['params']['requestId'])
                                try:
                                    requestId = log_json_object['message']['params']['requestId']
                                    networkResponses = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
                                    entityResponse = json.loads(networkResponses['body'])
                                except: continue

                                print(entityResponse)
                                if "businessViewInfo" in entityResponse:
                                    if "businessViewDetails" in entityResponse["businessViewInfo"]:
                                        print("Got response for businessRegNo: %s and busOrgNumber: %s ." % (entityResponse['businessViewInfo']['businessViewDetails']['businessRegNo'], str(busOrgNumber)))
                                        fileName = entityResponse['businessViewInfo']['businessViewDetails']['businessRegNo'] + '_' + str(busOrgNumber) + '.json'
                                        json_file_path = os.path.join(reportsPath, fileName)
                                        print(json_file_path)
                                        with open(json_file_path, "w") as file1:
                                            json.dump(entityResponse, file1)
                                            upd_check = artDb.update_the_record(todays_date, upd_recs[0][0], 'XSMUCBRDX')
                                            print(f"Records updated: {upd_check}")
                                            FOUND += 1
                                try:
                                    time.sleep(random.randint(2, 5))
                                    clickBtn = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="dialog-close-button"]')))
                                    driver.execute_script("arguments[0].click();", clickBtn)
                                except Exception as error:
                                    print("Encountered an Exception on click!")
                                    print(f"An exception occurred:{str(error)}")
                                break
                        time.sleep(random.randint(1, 3))
                    # try:
                    #     time.sleep(random.randint(3, 7))
                    #     nextPage = driver.find_element(By.XPATH, '//button[ contains(@class,"mat-paginator-navigation-next") and contains(@aria-label,"Next page")]')
                    #     driver.execute_script("arguments[0].click();", nextPage)
                    #     time.sleep(random.randint(1, 3))
                    # except Exception as error:
                    #     if page == totalPages:
                    #         print("Last Page Reached or got some issues...!")
                    #     else:
                    #         print("Faced some errors while crawling through the page...!")
                    #     print(f"An exception occurred:{str(error)}")
    time.sleep(random.randint(2, 6))
    driver.close()
    break
time.sleep(random.randint(1, 3))
exit()