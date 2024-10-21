import threading
import os
import shutil
from pathlib import Path
import datetime
import calendar
import json
from selenium.webdriver import DesiredCapabilities

import threading
from math import ceil

from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
import random
from selenium.common.exceptions import NoSuchElementException
import re
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from services import MessageService
from services import DbService
from services import StorageService
from settings import SERVICE
from settings import SELENIUMDRIVE

KEEP_ALIVE_PERIOD = 50

print(f" [{SERVICE['name']}] Starting...")

message_service = MessageService(SERVICE["queue"])
keep_alive_timer = None

SOURCE = "XSCAQCREG"

outputs = {}


def keep_alive_start():
    global keep_alive_timer
    print("Sending ++++Keep Alive++++")
    try:
        message_service.connection.process_data_events()
        keep_alive_timer = threading.Timer(50.0, keep_alive_start)
        keep_alive_timer.start()
    except Exception as e:
        print("Message service may be already down")
        print(str(e))


def keep_alive_stop():
    global keep_alive_timer
    if keep_alive_timer is not None:
        keep_alive_timer.cancel()


keep_alive_start()


def process_message():
    correlation_info = (
        response["correlation_info"] if "correlation_info" in response else None
    )
    step_configuration = (
        response["step_configuration"] if "step_configuration" in response else None
    )
    batch = correlation_info["batch"] if "batch" in correlation_info else None
    if not correlation_info or not step_configuration or not batch:
        raise Exception("response malformed")
    return correlation_info, step_configuration, batch

# ----------------------------------------------------------------------


def findDay(date):
    born = datetime.datetime.strptime(date, "%m/%d/%Y").weekday()
    return calendar.day_name[born]


def processLog(log):
    log = json.loads(log["message"])["message"]
    # print(log)
    if "Network.responseReceived" in log["method"] and "params" in log.keys():
        body = driver.execute_cdp_cmd(
            "Network.getResponseBody", {"requestId": log["params"]["requestId"]}
        )
        return body
    else:
        return None

def getCrawlingNewData(artDb, source_id, crawlingActiveLimit):
    print("Checking New data availablle: ")
    # crawlingActiveLimit = artDb.getCrawlingNumbersData(source_id,'UPDATE','ACTIVE')
    print("Crawling limit: %s" % crawlingActiveLimit)
    cursor = artDb.connection.cursor()
    cursor.execute(
        "SELECT NEQ FROM `XSCAQCREG_COMPARISONS_TABLE` WHERE `STATUS` = '1' ORDER BY THEID ASC LIMIT %s"
        % crawlingActiveLimit
    )
    result = cursor.fetchall()
    crawlingArr = []
    if cursor.rowcount > 0:
        # print(result)
        for rec in result:
            crawlingArr.append(rec[0])
        # print(crawlingArr)
        cursor.execute(
            f"UPDATE `XSCAQCREG_COMPARISONS_TABLE` SET STATUS='2' WHERE `STATUS` = '1' ORDER BY THEID ASC LIMIT {crawlingActiveLimit}"
        )
    return crawlingArr


def getCrawlingsDataForUpdate(artDb, source_id, crawlingActiveLimit, crawlingInactiveLimit):
    # crawlingActiveLimit = artDb.getCrawlingNumbersData(source_id,'UPDATE','ACTIVE')
    # crawlingInactiveLimit = artDb.getCrawlingNumbersData(source_id,'UPDATE','INACTIVE')
    arr = []
    updateRegIds = []
    cursor = artDb.connection.cursor()

    if crawlingActiveLimit > 0:
        print("Active Companies for Crawlings")
        active_sql = f"select entity_data_id, idkey as label from CRAWLINGS_XSCAQCREG_ACTIVE_DATA_VIEW where source_id={source_id} and active=1 limit {crawlingActiveLimit}"
        cursor.execute(active_sql)
        result = cursor.fetchall()
        for row in result:
            arr.append(row[1].replace("QC-", ""))
            updateRegIds.append(row[0])
        print(arr)
        print(updateRegIds)

    if crawlingInactiveLimit > 0:
        print("In-Active Companies for Crawlings")
        in_active_sql = f"select entity_data_id, idkey as label from CRAWLINGS_XSCAQCREG_INACTIVE_DATA_VIEW where source_id={source_id} and active=0 limit {crawlingInactiveLimit}"
        cursor.execute(in_active_sql)
        result = cursor.fetchall()
        for row in result:
            arr.append(row[1].replace("QC-", ""))
            updateRegIds.append(row[0])
        print(arr)
        print(updateRegIds)

    cursor.close()
    if len(updateRegIds) > 0:
        print(
            "Total Available Companies for Crawlings by Query = "
            + str(len(updateRegIds))
        )
        isUpdate = False
        inData = ""
        for key, isId in enumerate(updateRegIds):
            if key == len(updateRegIds) - 1:
                inData += "'" + str(isId) + "'"
            else:
                inData += "'" + str(isId) + "',"
                
        updateSql = (
            "UPDATE entity_data SET effective_date='"
            + str(datetime.date.today())
            + "' where source_id="
            + str(source_id)
            + " and id IN("
            + inData
            + ")"
        )
        cursor1 = artDb.connection.cursor()
        print(updateSql)
        cursor1.execute(updateSql)
        artDb.connection.commit()
        if cursor1.rowcount > 0:
            isUpdate = True
        # if data is not updated
        if isUpdate == False:
            arr = []
        print(arr)
        print(updateRegIds)

    print(
        f"Available Crawling Data Effective Date is updated into entity_data={len(updateRegIds)}"
    )
    return arr

def insert_or_update_records_status(artDb,label):
    cursor = artDb.connection.cursor()
    sql = f"select * from `XSCAQCREG_COMPARISONS_TABLE` where NEQ={label}"
    cursor.execute(sql)
    result = cursor.fetchall()
    try:
        cursor1 = artDb.connection.cursor()
        if cursor.rowcount > 0:
            cursor1.execute(f"UPDATE `XSCAQCREG_COMPARISONS_TABLE` SET STATUS='100' WHERE `NEQ` LIKE '{label}'")
            artDb.connection.commit()
            print(f"Record {label} Updated successfully ")
            cursor.close()
            cursor1.close()
            return True
        else:
            cursor1.execute(f"INSERT INTO `XSCAQCREG_COMPARISONS_TABLE`(`NEQ`,`STATUS`) VALUES ('{label}','100')")
            artDb.connection.commit()
            print(f"Record {label} Inserted successfully ")
            cursor.close()
            cursor1.close()
            return True
    except Exception as e:
        print("Error while updating or inserting record to table")
        print(e)
        return False
    
def getDriver():
    print("Getting User Agent...")
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    print(user_agent)
    print("Setting Capabilities...")
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    chrome_options = uc.options.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--dns-prefetch-disable")
    chrome_options.add_argument(f"--user-agent={user_agent}")
    chrome_options.add_argument("window-size=1920,1080")
    # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_options.arguments.extend(
        [
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--enable-javascript",
            "--disable-gpu",
        ]
    )
    print("Starting Driver...")
    # uc.TARGET_VERSION = 118
    driver = uc.Chrome(
        version_main=118,
        options=chrome_options,
        service_args=["--verbose"],
        use_subprocess=False,
        desired_capabilities=capabilities,
    )
    # driver.maximize_window()
    driver.delete_all_cookies()
    driver.execute_cdp_cmd(
        "Storage.clearDataForOrigin",
        {
            "origin": "*",
            "storageTypes": "all",
        },
    )
    # print(
    #     "url: https://www.registreentreprises.gouv.qc.ca/RQAnonymeGR/GR/GR03/GR03A2_19A_PIU_RechEnt_PC/PageRechSimple.aspx?T1.CodeService=S00436&Clng=F&WT.co_f=2ea39da008a15a1a9ca1664218982959'"
    # )
    # driver.get(
    #     "https://www.registreentreprises.gouv.qc.ca/RQAnonymeGR/GR/GR03/GR03A2_19A_PIU_RechEnt_PC/PageRechSimple.aspx?T1.CodeService=S00436&Clng=F&WT.co_f=2ea39da008a15a1a9ca1664218982959'"
    # )
    print(
        "https://www.registreentreprises.gouv.qc.ca/RQAnonymeGR/GR/GR03/GR03A2_19A_PIU_RechEnt_PC/PageRechSimple.aspx?T1.CodeService=S00436"
    )
    driver.get(
        "https://www.registreentreprises.gouv.qc.ca/RQAnonymeGR/GR/GR03/GR03A2_19A_PIU_RechEnt_PC/PageRechSimple.aspx?T1.CodeService=S00436"
    )
    wait = WebDriverWait(driver, random.randint(120, 130))
    print("Driver Started")
    
    return driver


while True:
    print(f" [{SERVICE['name']}] Getting new messages...")
    response: dict = message_service.get_work()
    t = time.time()
    FOUND = 0
    if response:
        correlation_info, step_configuration, batch = process_message()
        job_id = response["correlation_info"]["job"]

        S3storage = StorageService()
        artDb = DbService()

        source_id = artDb.get_source_id(SOURCE)
        # print(source_id)

        crawlingActiveLimit = artDb.getCrawlingNumbersData(
            source_id, "UPDATE", "ACTIVE"
        )
        crawlingInactiveLimit = artDb.getCrawlingNumbersData(
            source_id, "UPDATE", "INACTIVE"
        )

        newCrawlingData = getCrawlingNewData(artDb, source_id, crawlingActiveLimit)
        print("New companies available: %s" % len(newCrawlingData))
        print(newCrawlingData)

        if len(newCrawlingData) > 0:
            # a = newCrawlingData.pop(4)
            print(newCrawlingData)
            crawlingActiveLimit = crawlingActiveLimit - len(newCrawlingData)

            if crawlingActiveLimit > 0:
                res = getCrawlingsDataForUpdate(
                    artDb, source_id, crawlingActiveLimit, crawlingInactiveLimit
                )
                print(res)
                for item in res:
                    newCrawlingData.append(item)
                print(newCrawlingData)
        else:
            newCrawlingData = getCrawlingsDataForUpdate(
                artDb, source_id, crawlingActiveLimit, crawlingInactiveLimit
            )
            print(newCrawlingData)

        print(f"Total Crawling Available = {len(newCrawlingData)}")
        
        if len(newCrawlingData) == 0:
            print(f"No records for crawling")
            outputs["FOUND"] = FOUND
            print(outputs)
            message_service.finish_work(outputs)
            outputs = {}
            print(f" [{SERVICE['name']}] Time elapsed:", str(time.time() - t))
            break

        current_directory = os.getcwd()
        backupPath = f"{current_directory}/{job_id}/"
        if not os.path.exists(backupPath):
            os.makedirs(backupPath)
        print(f"Reports path: {backupPath}")
        screenShotPath = f"{current_directory}/screenshots/"
        if not os.path.exists(screenShotPath):
            os.makedirs(screenShotPath)
        print(f"Screenshots path: {screenShotPath}")

        FOUND = 0

        # ---------------------------------------------

        driver = getDriver()

        scrn = 0
        checkBoxChecked = False
        for label in newCrawlingData:
            print(f"Crawling {label}")
            
            driver.save_screenshot(f"{screenShotPath}screenie_{label}_{scrn}_1.png")
            screenShotFilePath = f"{screenShotPath}screenie_{label}_{scrn}_1.png"
            driver.save_screenshot(screenShotFilePath)
            shotSv = S3storage.save_screenshot(os, screenShotFilePath, f"screenie_{label}_{scrn}_1.png",job_id)
            if shotSv == True:
                print(f"image file moved to S3 todo : screenie_{label}_{scrn}_1.png")
                try:
                    os.remove(screenShotFilePath)
                except OSError:
                    pass
            
            firstTryOK = False
            try:
                field = WebDriverWait(driver,SELENIUMDRIVE['driverwaittime']).until(
                    EC.element_to_be_clickable(
                        (
                            By.ID,
                            "CPH_K1ZoneContenu1_Cadr_IdSectionRechSimple_IdSectionRechSimple_K1Fieldset1_ChampRecherche__cs",
                        )
                    )
                )
                driver.execute_script("arguments[0].value = arguments[1]", field, label)
                firstTryOK = True
            except Exception as e:
                print(e)
                print(f"Restarting driver...")
                driver.close()
                time.sleep(random.randint(1, 3))
                driver = getDriver()
            
            if firstTryOK == False:
                try:
                    field = WebDriverWait(driver,SELENIUMDRIVE['driverwaittime']).until(
                        EC.element_to_be_clickable(
                            (
                                By.ID,
                                "CPH_K1ZoneContenu1_Cadr_IdSectionRechSimple_IdSectionRechSimple_K1Fieldset1_ChampRecherche__cs",
                            )
                        )
                    )
                    driver.execute_script("arguments[0].value = arguments[1]", field, label)
                    firstTryOK = True
                except Exception as e:
                    print(e)
                    print(f"Data not found first request got failed")
                    print(f"Recorded in table : {insert_or_update_records_status(artDb,str(label))}")
                    print(f"File Not generated... for  label {label}")
                    scrn = scrn + 1
                    print(f"Restarting driver...")
                    driver.close()
                    time.sleep(random.randint(1, 3))
                    driver = getDriver()
                    continue

            time.sleep(random.randint(1, 3))
            if checkBoxChecked == False:
                button1 = WebDriverWait(driver,SELENIUMDRIVE['driverwaittime']).until(
                    EC.element_to_be_clickable(
                        (
                            By.ID,
                            "CPH_K1ZoneContenu1_Cadr_IdSectionRechSimple_IdSectionRechSimple_CondUtil_CaseConditionsUtilisation_0",
                        )
                    )
                )
                driver.execute_script("arguments[0].click();", button1)
                checkBoxChecked = True

            time.sleep(random.randint(1, 3))
            
            driver.save_screenshot(f"{screenShotPath}screenie_{label}_{scrn}_2.png")
            screenShotFilePath = f"{screenShotPath}screenie_{label}_{scrn}_2.png"
            driver.save_screenshot(screenShotFilePath)
            shotSv = S3storage.save_screenshot(os, screenShotFilePath, f"screenie_{label}_{scrn}_2.png",job_id)
            if shotSv == True:
                print(f"image file moved to S3 todo : screenie_{label}_{scrn}_2.png")
                try:
                    os.remove(screenShotFilePath)
                except OSError:
                    pass
                
            el = WebDriverWait(driver,SELENIUMDRIVE['driverwaittime']).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//input[@id='CPH_K1ZoneContenu1_Cadr_IdSectionRechSimple_IdSectionRechSimple_KRBTRechSimple_btnRechercher']",
                    )
                )
            )
            driver.execute_script("arguments[0].click();", el)
            time.sleep(random.randint(1, 3))
            driver.save_screenshot(f"{screenShotPath}screenie_{label}_{scrn}_3.png")
            screenShotFilePath = f"{screenShotPath}screenie_{label}_{scrn}_3.png"
            driver.save_screenshot(screenShotFilePath)
            shotSv = S3storage.save_screenshot(os, screenShotFilePath, f"screenie_{label}_{scrn}_3.png",job_id)
            if shotSv == True:
                print(f"image file moved to S3 todo : screenie_{label}_{scrn}_3.png")
                try:
                    os.remove(screenShotFilePath)
                except OSError:
                    pass
            
            dataSuccessFlag = False
            try:
                WebDriverWait(driver,SELENIUMDRIVE['driverwaittime']).until(EC.presence_of_element_located((By.XPATH,'//span[contains(.,"(NEQ)")]/parent::label/following-sibling::p')))
                cId = driver.find_element(
                    by=By.XPATH,
                    value='//span[contains(.,"(NEQ)")]/parent::label/following-sibling::p',
                ).text
                dataSuccessFlag = True
                print(cId)
            except Exception as e:
                print(f"First xpath not catch the NEQ identifier")
            if dataSuccessFlag == False:
                try:
                    print(f"//input[@value='{label}' and @type='text']")
                    WebDriverWait(driver,SELENIUMDRIVE['driverwaittime']).until(EC.presence_of_element_located((By.XPATH,f"//input[@value='{label}' and @type='text']")))
                    dataSuccessFlag = True
                except Exception as e2:
                    dataSuccessFlag = False
                    print(e2)
                    print(f"Data not found for this entity")
                    print(f"Recorded in table : {insert_or_update_records_status(artDb,str(label))}")
                    print(f"File Not generated... for  label {label}")
                    scrn = scrn + 1
                    continue
                
            htmlData = driver.page_source
            # print(content)
            time.sleep(random.randint(1, 3))
            en = WebDriverWait(driver,SELENIUMDRIVE['driverwaittime']).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//input[@id='CPH_K1ZoneContenu1_Cadr_Section00_Section00_K1RubanBoutonsRetour_btnBoutonGenerique01']",
                    )
                )
            )
            driver.execute_script("arguments[0].click();", en)
            
            driver.save_screenshot(f"{screenShotPath}screenie_{label}_{scrn}_4.png")
            screenShotFilePath = f"{screenShotPath}screenie_{label}_{scrn}_4.png"
            driver.save_screenshot(screenShotFilePath)
            shotSv = S3storage.save_screenshot(os, screenShotFilePath, f"screenie_{label}_{scrn}_4.png",job_id)
            if shotSv == True:
                print(f"image file moved to S3 todo : screenie_{label}_{scrn}_4.png")
                try:
                    os.remove(screenShotFilePath)
                except OSError:
                    pass
                
            # htmlData = curlReq(driver, label)
            if dataSuccessFlag == False:
                print(f"Recorded in table : {insert_or_update_records_status(artDb,str(label))}")
                print(f"File Not generated... for  label {label}")
                continue
            
            fileName = str(label) + ".html"
            localFilePath = backupPath + str(label) + ".html"
            f = open(localFilePath, "w")
            f.write(htmlData)
            f.close()

            fileSv = S3storage.save_file(os, localFilePath, fileName)
            if fileSv == True:
                print(f"file moved to S3 todo : {fileName}")
                try:
                    os.remove(localFilePath)
                except OSError:
                    pass

            FOUND = FOUND + 1
            scrn = scrn + 1
        try:
            print(f"closing Drvier...")
            driver.close()
        except Exception as error:
            print(f"Driver already closed.")
        
        try:
            backupPath = Path(backupPath)
            if backupPath.exists() and backupPath.is_dir():
                shutil.rmtree(backupPath)
        except OSError:
            pass

        time.sleep(random.randint(3, 5))
        artDb.close()
        # ---------------------------------------------
        outputs["FOUND"] = FOUND
        print(outputs)
        message_service.finish_work(outputs)
        outputs = {}
        print(f" [{SERVICE['name']}] Time elapsed:", str(time.time() - t))
    else:
        print(f" [{SERVICE['name']}] No messages, stopping..")
        break

print("closing message service...")
message_service.close()
keep_alive_stop()
exit()
