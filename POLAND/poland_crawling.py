from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from glob import glob
import os
from selenium.common.exceptions import NoSuchElementException
import shutil
from selenium.webdriver.support import expected_conditions as EC
from MySQLdb import _mysql
import MySQLdb
import time
import json
import os
import tempfile
from functools import reduce
import undetected_chromedriver as webdriver
import traceback
import requests
from win32com.client import Dispatch
import psutil
import subprocess
from win32com.client import Dispatch
current_directory = os.getcwd()


def delete_files_in_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Get the list of files in the folder
        files = os.listdir(folder_path)
        
        # Iterate over each file and delete it
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            os.remove(file_path)
            print(f"File '{file_path}' deleted.")
        
        print(f"All files in folder '{folder_path}' deleted.")
    else:
        print(f"Folder '{folder_path}' does not exist.")

def create_folder(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        # If not, create the folder
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")

create_folder('Todo')
create_folder('Done')

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


conf = open('poland.json')
conFile = json.load(conf)
print(conFile)
print(conFile['Browser'])
print(conFile['Machine_Name'])
print(conFile['Service'])

try:
    class ChromeWithPrefs(webdriver.Chrome):
        def __init__(self, *args, options=None, **kwargs):
            if options:
                self._handle_prefs(options)

            super().__init__(*args, options=options, **kwargs)

            # remove the user_data_dir when quitting
            self.keep_user_data_dir = False

        @staticmethod
        def _handle_prefs(options):
            if prefs := options.experimental_options.get("prefs"):
                # turn a (dotted key, value) into a proper nested dict
                def undot_key(key, value):
                    if "." in key:
                        key, rest = key.split(".", 1)
                        value = undot_key(rest, value)
                    return {key: value}

                # undot prefs dict keys
                undot_prefs = reduce(
                    lambda d1, d2: {**d1, **d2},  # merge dicts
                    (undot_key(key, value) for key, value in prefs.items()),
                )

                # create an user_data_dir and add its path to the options
                user_data_dir = os.path.normpath(tempfile.mkdtemp())
                options.add_argument(f"--user-data-dir={user_data_dir}")

                # create the preferences json file in its default directory
                default_dir = os.path.join(user_data_dir, "Default")
                os.mkdir(default_dir)

                prefs_file = os.path.join(default_dir, "Preferences")
                with open(prefs_file, encoding="latin1", mode="w") as f:
                    json.dump(undot_prefs, f)

                # pylint: disable=protected-access
                # remove the experimental_options to avoid an error
                del options._experimental_options["prefs"]


    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--window-size=1020,900")
    chrome_options.add_argument("--headless=new")
    # chrome_options.add_experimental_option("prefs", {"download.default_directory": "C:\\Users\\Lenovo\\Poland\\Todo\\"})
    prefs = {
        # "profile.default_content_setting_values.images": 2,
        "download.default_directory":  f"{current_directory}\\Todo\\",
        'profile.default_content_setting_values.automatic_downloads': 1
        # "plugins.always_open_pdf_externally": True,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # use the derived Chrome class that handles prefs
    driver = ChromeWithPrefs(options=chrome_options, version_main=major_version)

    # driver = uc.Chrome(options=chrome_options, use_subprocess=True)
    driver.maximize_window()

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

    def get_last_filename_and_rename(save_folder, new_filename):
        files = glob(save_folder + '\\*')
        max_file = max(files, key=os.path.getctime)
        filename, ext = os.path.splitext(os.path.basename(max_file))
        new_path = os.path.join(os.path.dirname(max_file), new_filename + ext)
        while True:
            try:
                os.rename(max_file, new_path)
                break  # If renaming is successful, exit the loop
            except PermissionError:
                print(traceback.format_exc())
                time.sleep(1)  # Wait for a second and try again
                continue
        print(new_path)
        newMovelocation = new_path.replace('Todo\\', 'Done\\')
        print(newMovelocation)
        shutil.move(new_path, newMovelocation)
        return new_path 

    db=_mysql.connect("localhost","root","","crawler_db")
    driver.get('https://ekrs.ms.gov.pl/rdf/pd/search_df')
    time.sleep(10)
    no_data = 0 
    for _ in range(20):
        requests.get('http://54.246.35.195/DEV2.0/Configrator/monitor.php?Browser='+conFile['Browser']+'&Service='+conFile['Service']+'&Machine_Name='+conFile['Machine_Name'])
        flag = True
        delete_files_in_folder('Todo')
        while flag:
            try:
                db.query("CALL PROCEDURE_URL_POLAND(@p0,@p1);")
                db.query('SELECT @p0 AS `theid`,@p1 AS `krs`')
                r=db.store_result()
                results=r.fetch_row()
                theid = results[0][0].decode()
                krs = results[0][1].decode()
                flag = False
            except:
                print(traceback.format_exc())
                continue
        try:
            wait = WebDriverWait(driver, 60)
            unlog = wait.until(EC.element_to_be_clickable((By.XPATH,'//input[contains(@class, "ui-inputtext")]')))
            driver.execute_script("arguments[0].value = arguments[1]", unlog, krs)
            time.sleep(3)
            m4 = wait.until(EC.element_to_be_clickable((By.ID,'unloggedForm:timeDelBtn')))
            driver.execute_script("arguments[0].click();", m4)
            front_page  = driver.page_source
        except:
            print(traceback.format_exc())
            driver.get('https://ekrs.ms.gov.pl/rdf/pd/search_df')
            continue  
        if "Brak dokumentów dla KRS" in front_page:
            no_data+=1
            if no_data<7:
                print('No data')
                db.query(f"UPDATE URL_POLAND SET STATUS=5 WHERE KRS={krs}")
            else:
                driver.get('https://ekrs.ms.gov.pl/rdf/pd/search_df')
            continue
        if "Wymagane oczekiwanie pomiędzy kolejnymi wywołaniami" in front_page:
            print('time limit or reloading page')
            driver.get('https://ekrs.ms.gov.pl/rdf/pd/search_df')
            continue
        try:
            time.sleep(3)
            m5 = wait.until(EC.element_to_be_clickable((By.ID,'unloggedForm:krs0')))
            driver.execute_script("arguments[0].click();", m5)
            front_page_1  = driver.page_source
        except:
            print(traceback.format_exc())
            driver.get('https://ekrs.ms.gov.pl/rdf/pd/search_df')
            continue  
        if "Brak dokumentów dla KRS" in front_page_1:
            no_data+=1
            if no_data<7:
                db.query(f"UPDATE URL_POLAND SET STATUS=5 WHERE KRS={krs}")
                print('No data')
            else:
                driver.get('https://ekrs.ms.gov.pl/rdf/pd/search_df')
            continue
        no_data=0
        if "Wymagane oczekiwanie pomiędzy kolejnymi wywołaniami" in front_page_1:
            print('time limit or reloading page')
            driver.get('https://ekrs.ms.gov.pl/rdf/pd/search_df')
            continue
        try:
            time.sleep(3)
            m6 = wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[@id="searchForm:docTable_data"]/tr/td[contains(text(),"Roczne sprawozdanie")]/following-sibling::td/a)[1]')))
            driver.execute_script("arguments[0].click();", m6)
            time.sleep(3)
            m7 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchForm:szczegolyPanel"]/tfoot/tr/td/div/a[1]')))
            driver.execute_script("arguments[0].click();", m7) 
            time.sleep(3)
            m8 = wait.until(EC.element_to_be_clickable((By.XPATH, '(//button[contains(@class, "ui-button-icon-only")])[1]')))
            driver.execute_script("arguments[0].click();", m8) 
        except:
            print(traceback.format_exc())
            driver.get('https://ekrs.ms.gov.pl/rdf/pd/search_df')
            continue        
        db.query(f"UPDATE URL_POLAND SET STATUS=10 WHERE KRS={krs}")
        time.sleep(8)
        get_last_filename_and_rename(f"{current_directory}\\Todo\\",krs )
except:
    print(traceback.format_exc())

finally:
    try:
        subprocess.run(["aws", "s3", "mv", "./Done/", f"s3://dev_buk/DATA/SOURCE/POLAND/XML/", "--recursive"], check=True)
    except: pass
    kill_chrome_process(driver)
    driver.quit()
    db.close()

    