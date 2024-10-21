from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
# from fake_useragent import UserAgent
import json
import math
import time
import random
from math import ceil
import mysql.connector
from mysql.connector import Error
import datetime
import os
import requests
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


current_directory = os.getcwd()
reportsPath = f"{current_directory}/Reports/"
if not os.path.exists(reportsPath):
    os.makedirs(reportsPath)
print(f"Reports path: {reportsPath}")

print("Setting Capabilities...")
capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {'performance': "ALL"}

uc.TARGET_VERSION = major_version
chrome_options = uc.options.ChromeOptions()
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{major_version} Safari/537.36"

chrome_options.add_argument('--dns-prefetch-disable')
chrome_options.add_argument(f'--user-agent={user_agent}')

chrome_options.add_argument("--headless=new")
# chrome_options.headless = False

print("Starting Driver...")
driver = uc.Chrome(version_main=major_version,options=chrome_options, use_subprocess=True, desired_capabilities=capabilities)
print("Driver Started")
driver.maximize_window()
print("url: https://cado.eservices.gov.nl.ca/")
driver.get('https://cado.eservices.gov.nl.ca/')
wait = WebDriverWait(driver, 120)

time.sleep(random.randint(1, 3))
print("searching companies search field...")
compSearch = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@id='Header1_lnkCompanies']")))
driver.execute_script("arguments[0].click();", compSearch)

time.sleep(random.randint(1, 3))
compSearch2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@href='CompanyNameNumberSearch.aspx']")))
driver.execute_script("arguments[0].click();", compSearch2)

conf = open('cado.json')
# returns JSON object as 
# a dictionary
conFile = json.load(conf)

#crawlingStrtRng = "11M"
# crawlingStrtRng <= 11 or
while  True: 

    index = 1
    while True:
        r = requests.get('http://34.240.143.117/Procedure//PROCEDURE_URL_XSCANLREG.php?action=GET')
        keyworddata = r.json()
        print(keyworddata['url'])
        crawlingStrtRng = keyworddata['url']
        time.sleep(random.randint(1, 3))
        driver.find_element(by=By.XPATH, value="//input[@id='txtCompanyNumber']").clear()
        time.sleep(random.randint(1, 3))
        print("Setting value search box...")
        driver.find_element(by=By.XPATH, value="//input[@id='txtCompanyNumber']").send_keys(crawlingStrtRng)

        print("Submitting request...")
        submit = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@id='btnSearch']")))
        driver.execute_script("arguments[0].click();", submit)

        absResult = False
        record_count = 0

        time.sleep(random.randint(2, 3))
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//table[@id='tableSearchResults']/tbody/tr/td[contains(.,'Records Found:')]/span")))
            recordCount = driver.find_element(By.XPATH, value="//table[@id='tableSearchResults']/tbody/tr/td[contains(.,'Records Found:')]/span")
            print(f"Records count: {recordCount.text}")
            record_count = recordCount.text
        except Exception as e:
            print(f"Didn't found count, verifying absolute result...")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//td[@class='CompanyNumberText']/span[@id='lblCompanyNumber']")))
            record = driver.find_element(By.XPATH, value="//td[@class='CompanyNumberText']/span[@id='lblCompanyNumber']")
            print(f"Record Found: CompanyNumber - {record.text}")
            if record.text != None and record.text != False:
                record_count = 1
                absResult = True


        # time.sleep(random.randint(3, 5))
        # records = driver.find_element(By.XPATH, value="//td[contains(text(),'Records Found:')]/../following-sibling::tr/descendant::tr[contains(@class,'tablehead')]/following-sibling::tr[contains(@class,'row')]/td/a")

        if int(record_count) >= index and absResult == False:
            record = driver.find_element(By.XPATH, value=f"//td[contains(text(),'Records Found:')]/../following-sibling::tr/descendant::tr[contains(@class,'tablehead')]/following-sibling::tr[contains(@class,'row')][{index}]/td/a")
            print(f"Entity name : {record.text}")
            time.sleep(random.randint(3, 5))
            entityClick = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, f"//td[contains(text(),'Records Found:')]/../following-sibling::tr/descendant::tr[contains(@class,'tablehead')]/following-sibling::tr[contains(@class,'row')][{index}]/td/a")))
            driver.execute_script("arguments[0].click();", entityClick)
            time.sleep(random.randint(2, 4))
            
            htmlData = driver.page_source
            
            ## Handle Directors info
            currentDirectorList = False
            try:
                checkCurrentDirectors = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, f"//table/tbody/tr[@class='bluebar' and contains(.,'Current Directors')]")))
                currentDirectorList = True
            except Exception as e:
                pass
            
            if currentDirectorList == True:
                currentDirectorCount = 0
                try:
                    checkCurrentDirectorsCount = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, f"//table/tbody/tr[@class='bluebar' and contains(.,'Current Directors')]/following-sibling::tr/td[contains(text(),'Records Found:')]/span")))
                    currentDirectorCount = checkCurrentDirectorsCount.text
                except Exception as e:
                    pass
                print(f"Directors count = {currentDirectorCount}")
                if int(currentDirectorCount) > 10:
                    directorPageCounter = math.ceil( int(currentDirectorCount) / 10 ) - 1
                    directorsList = ""
                    directorsList = directorsList + f"<table class='currentDirectorsList'><tbody><tr>" # start creating list for currentDirectors for HTML document
                    while  directorPageCounter > 0:
                        time.sleep(random.randint(2, 4))
                        try:
                            currDirNextBtn = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, f"//table/tbody/tr[@class='bluebar' and contains(.,'Current Directors')]/following-sibling::tr[@id='trDirectorNav']/td/a[@id='lbtNext']")))
                            driver.execute_script("arguments[0].click();", currDirNextBtn)
                            time.sleep(random.randint(2, 4))
                            dirXpath = f"//table/tbody/tr[@class='bluebar' and contains(.,'Current Directors')]/following-sibling::tr[position()>2 and position()<{ (int(currentDirectorCount) % 10) +3}]"
                            currDir = driver.find_elements(By.XPATH, dirXpath)
                            for element in currDir:
                                print(f"{element.text}")
                                directorsList = directorsList + f"<td>{element.text}</td>"
                            
                        except Exception as e:
                            print(e)
                            print(f"Error in locating currentDirectors list!")
                            pass
                        
                        directorPageCounter = directorPageCounter - 1
                    directorsList = directorsList + f"</tr></tbody></table>"
                    htmlData = htmlData + directorsList# # close the last table to make it a complete HTML document
                else:
                    print(f"Directors less than 10")
                
            
            # htmlData = driver.page_source
            #htmlData = htmlData + directorsList
            
            companyNumber = driver.find_element(By.XPATH, value=f"//td[@class='CompanyNumberText']/span")
            print(f"Entity's companyNumber : {companyNumber.text}")
            label = companyNumber.text
            fileName = str(label) + ".html"
            localFilePath = reportsPath + str(label) + ".html"
            f = open(localFilePath, "w")
            requests.get('http://34.240.143.117/Procedure//PROCEDURE_URL_XSCANLREG.php?action=UPDATE&url='+crawlingStrtRng)
            f.write(htmlData)
            f.close()
            time.sleep(random.randint(3, 5))
            returnBack = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//a[@id='hylClose']")))
            driver.execute_script("arguments[0].click();", returnBack)

            time.sleep(random.randint(2, 3))
            index = index + 1
        elif absResult == True:
            print(f"Entity's companyNumber : {record.text}")
            label = record.text
            htmlData = driver.page_source
            
            ## Handle Directors info
            currentDirectorList = False
            try:
                checkCurrentDirectors = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, f"//table/tbody/tr[@class='bluebar' and contains(.,'Current Directors')]")))
                currentDirectorList = True
            except Exception as e:
                pass
            
            if currentDirectorList == True:
                currentDirectorCount = 0
                try:
                    checkCurrentDirectorsCount = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, f"//table/tbody/tr[@class='bluebar' and contains(.,'Current Directors')]/following-sibling::tr/td[contains(text(),'Records Found:')]/span")))
                    currentDirectorCount = checkCurrentDirectorsCount.text
                except Exception as e:
                    pass
                print(f"Directors count = {currentDirectorCount}")
                if int(currentDirectorCount) > 10:
                    directorPageCounter = math.ceil( int(currentDirectorCount) / 10 ) - 1
                    directorsList = ""
                    directorsList = directorsList + f"<table class='currentDirectorsList'><tbody><tr>" # start creating list for currentDirectors for HTML document
                    while  directorPageCounter > 0:
                        time.sleep(random.randint(2, 4))
                        try:
                            currDirNextBtn = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, f"//table/tbody/tr[@class='bluebar' and contains(.,'Current Directors')]/following-sibling::tr[@id='trDirectorNav']/td/a[@id='lbtNext']")))
                            driver.execute_script("arguments[0].click();", currDirNextBtn)
                            time.sleep(random.randint(2, 4))
                            dirXpath = f"//table/tbody/tr[@class='bluebar' and contains(.,'Current Directors')]/following-sibling::tr[position()>2 and position()<{ (int(currentDirectorCount) % 10) +3}]"
                            currDir = driver.find_elements(By.XPATH, dirXpath)
                            for element in currDir:
                                print(f"{element.text}")
                                directorsList = directorsList + f"<td>{element.text}</td>"
                            
                        except Exception as e:
                            print(e)
                            print(f"Error in locating currentDirectors list!")
                            pass
                        
                        directorPageCounter = directorPageCounter - 1
                    directorsList = directorsList + f"</tr></tbody></table>" # close the last table to make it a complete HTML document
                    htmlData = htmlData + directorsList
                else:
                    print(f"Directors less than 10")
                    
            # htmlData = driver.page_source
            
            
            fileName = str(label) + ".html"
            localFilePath = reportsPath + str(label) + ".html"
            f = open(localFilePath, "w")
            requests.get('http://34.240.143.117/Procedure//PROCEDURE_URL_XSCANLREG.php?action=UPDATE&url='+crawlingStrtRng)
            f.write(htmlData)
            f.close()
            time.sleep(random.randint(3, 5))
            returnBack = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//a[@id='hylClose']")))
            driver.execute_script("arguments[0].click();", returnBack)
            time.sleep(random.randint(1, 2))
            break
        else:
            break
        requests.get('http://54.246.35.195/DEV2.0/Configrator/monitor.php?Browser='+conFile['Browser']+'&Service='+conFile['Service']+'&Machine_Name='+conFile['Machine_Name'])
        time.sleep(random.randint(10, 15))
driver.close()
driver.quit()
    # exit()
    # crawlingStrtRng = crawlingStrtRng + 1


# //td[contains(text(),'Records Found:')]/../following-sibling::tr[contains(.,'Name') and contains(.,'Status') and contains(.,'Number')]/descendant::td/a/@href

# //span[@id='lblRecordsFound']/text()


# time.sleep(random.randint(3, 5))
# driver.close()