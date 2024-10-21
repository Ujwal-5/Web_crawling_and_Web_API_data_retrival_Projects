import logging
from MySQLdb import _mysql
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
import os
from selenium.webdriver.common.keys import Keys
from twocaptcha import TwoCaptcha
from lxml import etree
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
import shutil
import signal

def handle_signal(signum, frame):
    try:driver.quit()
    except:pass
    try:db.close()
    except:pass

signal.signal(signal.SIGTERM, handle_signal)

log_file = "hklog.log"
logging.basicConfig(filename=log_file, level=logging.INFO,format='%(asctime)s %(levelname)s: %(message)s')
logging.info("Starting script and connecting database using credential")
# pytesseract.pytesseract.tesseract_cmd = "tesseract.exe"

#-----------------------------------------------------------------

def process_page(content):
  if "Business Registration No." in content:
    BusinessNo = html_tree.xpath("//td[contains(text(), 'Business Registration No.')]/following-sibling::td/text()")
    print(BusinessNo[0].strip())
    ds_list.append("BUSINESSNO")
    vl_list.append(BusinessNo[0].strip())
  if "Name of Business / Corporation (Chinese)" in content:
    ChineseName = html_tree.xpath("//td[contains(text(), 'Name of Business / Corporation (Chinese)')]/following-sibling::td/text()")
    print(ChineseName[0].strip())
    ds_list.append("CHINESE_NAME")
    vl_list.append(ChineseName[0].strip())
  if "Name of Business / Corporation (English)" in content:
    EnglishName = html_tree.xpath("//td[contains(text(), 'Name of Business / Corporation (English)')]/following-sibling::td/text()")
    print(EnglishName[0].strip())
    ds_list.append("ENGLISH_NAME")
    vl_list.append(EnglishName[0].strip())
  if "Previously Known as (English)" in content:
    EnglishPrevName = html_tree.xpath("//td[contains(text(), 'Previously Known as (English)')]/following-sibling::td/text()")
    print(EnglishPrevName[0].strip())
    ds_list.append("ENGLISH_PREV_NAME")
    vl_list.append(EnglishPrevName[0].strip())
  if "Previously Known as (Chinese)" in content:
    ChinesePrevName = html_tree.xpath("//td[contains(text(), 'Previously Known as (Chinese)')]/following-sibling::td/text()")
    print(ChinesePrevName[0].strip())
    ds_list.append("CHINESE_PREV_NAME")
    vl_list.append(ChinesePrevName[0].strip())
  if "Branch Name (Chinese)" in content:
    ChineseBranchName = html_tree.xpath("//td[contains(text(), 'Branch Name (Chinese)')]/following-sibling::td/text()")
    print(ChineseBranchName[0].strip())
    ds_list.append("CHINESE_BRANCH_NAME")
    vl_list.append(ChineseBranchName[0].strip())
  if "Branch Name (English)" in content:
    EnglishBranchName = html_tree.xpath("//td[contains(text(), 'Branch Name (English)')]/following-sibling::td/text()")
    print(EnglishBranchName[0].strip())
    ds_list.append("ENGLISH_BRANCH_NAME")
    vl_list.append(EnglishBranchName[0].strip())
  if "Previous Business Name (Chinese)" in content:
    ChinesePrevBusinessName = html_tree.xpath("//td[contains(text(), 'Previous Business Name (Chinese)')]/following-sibling::td/text()")
    print(ChinesePrevBusinessName[0].strip())
    ds_list.append("CHINESE_PREV_BUSINESS_NAME")
    vl_list.append(ChinesePrevBusinessName[0].strip())
  if "Previous Business Name (English)" in content:
    EnglishPrevBusinessName = html_tree.xpath("//td[contains(text(), 'Previous Business Name (English)')]/following-sibling::td/text()")
    print(EnglishPrevBusinessName[0].strip())
    ds_list.append("ENGLISH_PREV_BUSINESS_NAME")
    vl_list.append(EnglishPrevBusinessName[0].strip())
  if "Business Name (Chinese)" in content:
    ChineseBusinessName = html_tree.xpath("//td[contains(text(), 'Business Name (Chinese)')]/following-sibling::td/text()")
    print(ChineseBusinessName[0].strip())
    ds_list.append("CHINESE_BUSINESS_NAME")
    vl_list.append(ChineseBusinessName[0].strip())
  if "Business Name (English)" in content:
    EnglishBusinessName = html_tree.xpath("//td[contains(text(), 'Business Name (English)')]/following-sibling::td/text()")
    print(EnglishBusinessName[0].strip())
    ds_list.append("ENGLISH_BUSINESS_NAME")
    vl_list.append(EnglishBusinessName[0].strip())
  logging.info('appending detail page to main page')
  f = open(f"{name}.html", "a", encoding="utf-8")
  f.write(content)
  f.close()

#--------------------------------------------------------------------

def captcha_solver():
    logging.info('Locating captcha image')
    captcha_image = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='captcha_image']")))
    
    try:
        logging.info('Capturing captcha screenshot')
        captcha_image.screenshot('captcha.png')
        print('screenshot taken')
    except KeyboardInterrupt:
        print("Loop interrupted by keyboard")
        logging.info('Exit')
        db.close()
        driver.quit()
    except WebDriverException:
        logging.info('WebDriverException occurred. Reloading captcha and calling captcha_solver()')
        reload = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href[contains(., 'javascript:reloadCaptcha()')]]")))
        driver.execute_script("arguments[0].click();", reload)
        print('Captcha reloaded')
        captcha_solver()
    
    logging.info('Locating virtual keyboard keys')
    images = driver.find_elements(By.XPATH, "//div[@class='keyboard__keys']//img")
    for index, image in enumerate(images, start=1):
        image.screenshot(f'{index}.png')
    
    count = 0
    logging.info('Solving captcha using 2captcha with retries')
    while count <= 3:
        try:
            result = solver.normal('captcha.png')
            captcha_text = result['code'].replace(' ', '').upper()
            print('Solved: ' + str(captcha_text))
            break
        except KeyboardInterrupt:
            print("Loop interrupted by keyboard")
            logging.info('Exit')
            db.close()
            driver.quit()
        except Exception as e:
            logging.error("An error occurred: %s", str(e))
            print(e)
            count += 1
            continue
    
    logging.info('Fetching keyboard button images using pytesseract')
    key_dict = {}
    for i in range(1, 10):
        image = Image.open(f'{i}.png')
        try:
            image = image.convert('L')
        except: pass
        threshold_value = 128
        image = image.point(lambda x: 0 if x < threshold_value else 255, '1')
        custom_config = r'--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        text = pytesseract.image_to_string(image, config=custom_config).strip()
        key = text[:1].upper()
        print(key)
        key_dict[i] = key
    
    logging.info('Reversing the key-value pairs')
    reversed_dict = {value: key for key, value in key_dict.items()}   
    result_key = []
    filtered_list = list(captcha_text)
    
    logging.info('Retrieving key from value')
    for value in filtered_list:
        try:
            key = reversed_dict.get(value)
            result_key.append(key)
        except KeyboardInterrupt:
            print("Loop interrupted by keyboard")
            logging.info('Exit')
            db.close()
            driver.quit()
        except Exception as e:
            logging.error("An error occurred: %s", str(e))
            pass
    
    # Printing the result
    print('result_key:', result_key)  # Output: key2
    print('filtered:', filtered_list)
    
    logging.info('Checking if filtered value is less than 4 and reloading captcha')
    if len(filtered_list) < 4 or None in result_key:
        reload = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href[contains(., 'javascript:reloadCaptcha()')]]")))
        driver.execute_script("arguments[0].click();", reload)
        print('Reload: result_key:', result_key, 'filtered_list:', filtered_list)
        captcha_solver()
    else:
        logging.info('Pressing keyboard buttons according to result_key values')
        for i in result_key:
            button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='keypad']/div/div/button[{i}]")))
            driver.execute_script("arguments[0].click();", button)
        
        logging.info('Clicking the submit button')
        submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='buttonArea']/div/a[3]")))
        driver.execute_script("arguments[0].click();", submit)
        print('Submitted')
    return captcha_text
#------------------------------------------------------------------------------------

def wait_for_page_load(driver):
  WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@id="logobarcolL"]/img')))

#--------------------------------------------------------------------------------
def setup_driver():
    options = Options()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--window-size=1020,900")
    chrome_options.add_argument('--dns-prefetch-disable')
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--headless=new")
    return uc.Chrome(options=chrome_options, use_subprocess=True)

#---------------------------------------------------------------------------------

while True:
  try:
    logging.info("Setting up chrome browser")
    start2= time.time()
    driver = setup_driver()
    driver.implicitly_wait(30)

    logging.info('loading hk page')
    driver.get('http://www.gov.hk/en/apps/irdbrnenquiry.htm')
    frame = driver.find_element(By.XPATH, "//frame[@noresize='noresize']")
    driver.switch_to.frame(frame)
    wait = WebDriverWait(driver, 30)

    logging.info('clicking begin application button')
    
    Begin_Application = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='buttonArea']/div/a")))
    driver.execute_script("arguments[0].click();", Begin_Application)

    logging.info('clicking agree application button')
    agree = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='buttonArea']/div/a[2]")))
    driver.execute_script("arguments[0].click();", agree)

    logging.info('clicking first option and clicking continue')
    tick = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='BRE']")))
    driver.execute_script("arguments[0].click();", tick)
    continu = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='buttondefault']")))
    driver.execute_script("arguments[0].click();", continu)
  
    while True:
      logging.info('fetching all records from XSHKBRN table')
      db=_mysql.connect("localhost","root","","crawler_db")
      flag = True
      print('before flag')
      ST = time.time()
      while flag:
        try:
            db.query('CALL `XSHKBRN`(@p0, @p1); ')
            db.query("SELECT @p0 AS `theid`, @p1 AS `name`;")
            flag = False
        except Exception as e: 
           logging.error(e)
           continue
      r=db.store_result()
      results=r.fetch_row()
      ED = time.time()
      TE = ED -ST
      print("Time taken to get procedure output", TE)
      logging.info('Time taken to get procedure output: %s', TE)
      logging.info('decoding name and theid')
      print(results)
      theid = results[0][0].decode()
      name = results[0][1].decode()

      logging.info('filling company_name from db')
      company_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@title='Please enter full Company Name']")))
      print(name)
      driver.execute_script("arguments[0].value = arguments[1]", company_name, name)

      logging.info('selecting all area from dropdown')
      grbf = Select(driver.find_element(By.XPATH,"//select[@name='businessAddArea']"))
      grbf.select_by_visible_text('ALL AREAS')

      logging.info('setting up 2captcha')
      api_key = os.getenv('APIKEY_2CAPTCHA', 'your_2captcha_key')
      solver = TwoCaptcha(api_key)

      stop2= time.time()
      time_taken2= stop2-start2
      print('Time taken to open bowser travel thorough captcha page and fill infomation: %s', time_taken2)
      logging.info('Time taken to open bowser travel thorough captcha page and fill infomation: %s', time_taken2)


      logging.info('looping to solve captcha')
      status = 0
      start = time.time()
      while True:
          print('while loop')
          driver.implicitly_wait(30)
          page = driver.page_source
          if ('Please select the verification code in order' in page and 'Re-Enter' not in page and status ==0 )or ('Error found in the inputted characters. Please re-select the characters as shown in the image.' in page and 'Re-Enter' not in page):
            print('captcha_solver')
            status = 1
            print(3)
            start1= time.time()
            catcha_value = captcha_solver()
            stop1 =time.time()
            print("Time taken for captcha solve:", stop1-start1)
            time_taken1 = stop1 - start1
            # Log the message
            logging.info('Time taken for captcha solving: %s', time_taken1)
          else:
            print('break')
            # Define the source file and new file names
            source_file = "captcha.png"

            new_file_name = f"{catcha_value}.png"

            # Define the destination folder
            destination_folder = "Captcha"

            # Rename the file
            new_file_path = os.path.join(os.path.dirname(source_file), new_file_name)
            os.rename(source_file, new_file_path)

            # Move the file to the destination folder
            destination_path = os.path.join(destination_folder, new_file_name)
            shutil.move(new_file_path, destination_path)
            break

          logging.info('captcha solved!')


      start3= time.time()
      try:  
        wait_elements = wait.until(EC.element_to_be_clickable((By.XPATH, "//table[@class='contenttext']/descendant::tr/descendant::td/a[@href]")))
        elements = driver.find_elements(By.XPATH, "//table[@class='contenttext']/descendant::tr/descendant::td/a[@href]")
        main_content = driver.page_source
        f = open(f"{name}.html", "w", encoding="utf-8")
        f.write(main_content)
        f.close()
        k=0
      except KeyboardInterrupt:
        print("Loop interrupted by keyboard")
        logging.info('Exit')
        db.close
        driver.quit()
      except TimeoutException:
        logging.info('inside except block, TimeoutException, no data setting k=1')
        k=1
        print('No Data')
        pass
      logging.info('Html saved')


      if k==1:
        logging.info('inside if loop, updateing status=7 since there is no data and setting j=2')
        status = "UPDATE crawler_db.XSHKBRN_TEMP_CRAWL SET UPDATEDAT = CURRENT_DATE, STATUS=7 WHERE THEID = '%s'" % (theid)
        db.query(status)
        db.commit()
        db.close()
        j=2
      else:
        # Iterate and click on each element
        j=1
        for i in range(len(elements)):
            # Re-find the elements after each navigation back
            elements = driver.find_elements(By.XPATH, "//table[@class='contenttext']/descendant::tr/descendant::td/a[@href]")
            # Check if the index is within the valid range
            if i < len(elements):
                # Click on the current element
                element = elements[i]
                driver.execute_script("arguments[0].click();", element)
                main_html_tree = etree.HTML(main_content)
                addr = main_html_tree.xpath(f"//table[descendant::tr/td[contains(.,'Record No.')]]/descendant::tr[{10+i}]/td/a/text()")
                logging.info('inside try: address = ' '.join(addr[0].split()) ,1 of the place where currently script stops')
                address = ' '.join(addr[0].split())
                vl_list = [address]
                ds_list = ["ADDR"]
                logging.info('detail page crawling')
                content=driver.page_source
                html_tree = etree.HTML(content)
                ds_list.append("CID")
                vl_list.append(theid)
                ds_list.append("NAME")
                vl_list.append(name)
                process_page(content)
                logging.info('appended detail page to main page')

                #Formating and inserting value to database
                logging.info('Formating and inserting value to a database')
                query_placeholders = ", ".join(['%s'] * len(vl_list))
                query_columns = ", ".join(ds_list)   
                formatted_values = ','.join(['"' + value.strip("'") + '"' for value in vl_list])
                insert_query = '''INSERT INTO XSHKBRN1 (%s) VALUES (%s) ''' %(query_columns, formatted_values) 
                print(insert_query)
                db.query("set names utf8;")
                db.query('SET NAMES utf8;')
                db.query('SET CHARACTER SET utf8;')
                db.query('SET character_set_connection=utf8;')
                db.query(insert_query)
                logging.info('Insertion successful')

                logging.info('Status updating...')
                if 'There is NO matching record' in content:
                  logging.info('setting Status=2, There is NO matching record')
                  status = "UPDATE crawler_db.XSHKBRN_TEMP_CRAWL SET UPDATEDAT = CURRENT_DATE, STATUS=2 WHERE THEID = '%s'" % (theid)
                  db.query()
                else:
                  if len(elements) == i+1:
                    logging.info('Setting STATUS=10, successful')
                    status = "UPDATE crawler_db.XSHKBRN_TEMP_CRAWL SET UPDATEDAT = CURRENT_DATE, STATUS = 10 WHERE THEID ='%s'" % (theid) 
                  else: 
                    logging.info('Setting STATUS=5, unsuccessful')
                    status = "UPDATE crawler_db.XSHKBRN_TEMP_CRAWL SET UPDATEDAT = CURRENT_DATE, STATUS=5 WHERE THEID = '%s'" % (theid)
                db.query(status)
                db.commit()

                logging.info('Clicking back button..')
                wait1 = WebDriverWait(driver, 30)
                back = wait1.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='buttonmenubox_R']/a[@alt='Back']")))
                driver.implicitly_wait(30)
                driver.execute_script("arguments[0].click();", back)
                driver.implicitly_wait(30)

      logging.info('Clcking RE-ENTER button..')
      source_file = f"{name}.html"
      destination_folder = "html"
      file_name = os.path.basename(source_file)
      destination_path = os.path.join(destination_folder, file_name)
      shutil.move(source_file, destination_path)
      re_enter = driver.find_element(By.XPATH,f"//*[@id='buttonArea']/div/a[{j}]")
      driver.execute_script("arguments[0].click();", re_enter)
      db.close()
      stop = time.time()
      time_taken = stop-start
      print('Time taken solve captcha and crawl informaion',time_taken) 
      logging.info('logging RE-ENTER sucessful: %s',time_taken)

  except Exception as e:
    logging.error("An error occurred: %s", str(e))
    print(e)
    try:
      logging.info('trying driver to close')
      driver.close()
    except Exception as e:
       logging.error("inside main except block within another except block, An error occurred: %s", str(e))
       pass
    pass

signal.pause()

