from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess
import subprocess
import random
import time
from MySQLdb import _mysql
from datetime import datetime
import sys
from lxml import html
import traceback


db = _mysql.connect("localhost","root", "", "crawler_db")      
website_url = "https://www.pxw2.snb.ca/card_online/Search/search.aspx"

chrome_command = "chrome.exe"
remote_debugging_port = "--remote-debugging-port=9224"
user_data_dir = "--user-data-dir=C:\\Scripts\\CANBREG\\slenium_based\\chrome_data"

# Combine the command and arguments into a list
command_list = [chrome_command, remote_debugging_port, user_data_dir, website_url]
# Redirect output and error to a log file
log_file = "logfile.txt"
with open(log_file, "w") as log:
    # Start Chrome as a background process
    process = subprocess.Popen(command_list, stdout=log, stderr=log, shell=False)

# Give some time for Chrome to start
input("Press Enter to continue...")

chrome_driver_path = "chromedriver.exe"
service = webdriver.chrome.service.Service(chrome_driver_path)

# Use webdriver.ChromeOptions() instead of deprecated chrome_options
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "localhost:9224")

# Create the WebDriver instance
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 30)  # Adjust the timeout as needed
# flag = True
# print('before flag')
# while flag:
#     try:
#         db.query('CALL `PROCEDURE_KEYWORDS_2_CANBREG`(@p0, @p1); ')
#         db.query("SELECT @p0 AS `id`, @p1 AS `keyword`;")
#         flag = False
#     except Exception as e: 
#         print(e)
#         continue
# r=db.store_result()
# results=r.fetch_row()

# print(results)
# id = results[0][0].decode()
keyword = input("Enter keyword here: ")#results[0][1].decode()
print(keyword)

last_number = 1

while True:
    try:
        html_content = driver.page_source
        tree = html.fromstring(html_content)
        internal_number = tree.xpath('//td/span/text()')[0]
        last_str = tree.xpath('//tr[@class="gvPager"]//td[last()]/a/text()')
        try:
            print(f"Extracted Last str: {last_str[0]}")
            if last_str[0].isdigit():
                last_number = int(last_str[0])
                print(f"Extracted Last number: {last_number}")
        except:
            pass
        print(f"Extracted number: {internal_number}")
        # Click using JavaScript
        if last_number==internal_number:

            with open(f"html/{keyword}_{int(internal_number)}.html", "w", encoding="utf-8") as file:
                file.write(html_content)

            print(f'{keyword}_{int(internal_number)} is saved!')
            current_time = datetime.now()
            query = f"UPDATE KEYWORDS_2_CANBREG SET FLAG = 10, updatedAt = '{current_time}', PAGE = {int(internal_number)} WHERE KEYWORD = '{keyword}'"
            db.query(query)
            break

        next_page = int(internal_number) + 1
        current_page = f"//td[contains(a/@href, 'Page${next_page}')]"
        print(current_page)
        page = wait.until(EC.element_to_be_clickable((By.XPATH, current_page)))
        time.sleep(3)
        page.click()
        time.sleep(3)
        with open(f"html/{keyword}_{int(internal_number)}.html", "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f'{keyword}_{int(internal_number)} is saved!')
        current_time = datetime.now()
        query = f"UPDATE KEYWORDS_2_CANBREG SET FLAG = 5, updatedAt = '{current_time}', PAGE = {int(internal_number)} WHERE KEYWORD = '{keyword}'"
        db.query(query)


    except Exception as e : 
        traceback.print_exc()
        print("Exception has occured!")
        chrome_driver_path = "chromedriver.exe"
        service = webdriver.chrome.service.Service(chrome_driver_path)
        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", "localhost:9224")
        driver = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(driver, 30) 

