from driver_config import DriverConf
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from lxml import html
from selenium.webdriver.support.ui import Select
from folder import create_folder
from settings import MYSQL, AWS
from database import DbService
from bs4 import BeautifulSoup
import traceback
import random
from s3_move import move_files
from moniter import hit_moniter_api
from selenium.webdriver.common.keys import Keys
# from DrissionPage import ChromiumPage
import time
from DrissionPage import ChromiumOptions, ChromiumPage
import traceback
import os,urllib,random,pydub,speech_recognition,time
from DrissionPage.common import Keys
import traceback
import sys

class RecaptchaSolver:
    def __init__(self, driver:ChromiumPage):
        self.driver = driver
    
    def solveCaptcha(self):
        iframe_inner = self.driver("@title=reCAPTCHA")
        time.sleep(0.1)
        
        # Click on the recaptcha
        iframe_inner('.rc-anchor-content',timeout=1).click()
        self.driver.wait.ele_displayed("xpath://iframe[contains(@title, 'recaptcha')]",timeout=3)

        # Sometimes just clicking on the recaptcha is enough to solve it
        if self.isSolved():
            return
        
        
        # Get the new iframe
        iframe = self.driver("xpath://iframe[contains(@title, 'recaptcha')]")
        print(iframe)
        # Click on the audio button
        try:
         iframe('#recaptcha-audio-button',timeout=5).click()
        except: 
            print(traceback.print_exc())
            iframe = self.driver("xpath://iframe[contains(@title, 'recaptcha')]")

        time.sleep(3)
        print(iframe)
        
        # Get the audio source
        src = iframe('#audio-source').attrs['src']
        print(src)
        print('hi')
        
        # Download the audio to the temp folder
        path_to_mp3 = os.path.normpath(os.path.join((os.getenv("TEMP") if os.name=="nt" else "/tmp/")+ str(random.randrange(1,1000))+".mp3"))
        path_to_wav = os.path.normpath(os.path.join((os.getenv("TEMP") if os.name=="nt" else "/tmp/")+ str(random.randrange(1,1000))+".wav"))
        print(path_to_mp3)
        print(path_to_wav)
        urllib.request.urlretrieve(src, path_to_mp3)

        # Convert mp3 to wav
        sound = pydub.AudioSegment.from_mp3(path_to_mp3)
        sound.export(path_to_wav, format="wav")
        sample_audio = speech_recognition.AudioFile(path_to_wav)
        r = speech_recognition.Recognizer()
        with sample_audio as source:
            audio = r.record(source)
        
        # Recognize the audio
        key = r.recognize_google(audio)
        print(key)
        if key == '':
            page.quit()
            sys.exit()

        
        # Input the key
        iframe('#audio-response').input(key.lower())
        time.sleep(0.1)
        
        # Submit the key
        iframe('#audio-response').input(Keys.ENTER)
        time.sleep(.4)

        # Check if the captcha is solved
        if self.isSolved():
            return
        else:
            raise Exception("Failed to solve the captcha")

    def isSolved(self):
        try:
            check_mark =  self.driver.ele(".recaptcha-checkbox-checkmark",timeout=3).attrs
            print(check_mark)
            return 'style' in check_mark 
        except:
            return False
        
try:
    co = ChromiumOptions()
    co.headless()  # 无头模式
    co.set_argument('--no-sandbox')
    page = ChromiumPage(co)
    recaptchaSolver = RecaptchaSolver(page)

    # 访问网页 (Visit a webpage)
    page.get("https://www.rp.gob.pa/LoginUsuario")
    time.sleep(5)
    # 输入文本 (Input text)
    page('#itNombreUsuario').input('nultalorza@gufum.com')
    time.sleep(2)
    page('@type=password').input('Food@123')
    time.sleep(3)
    t0 = time.time()
    try:
        recaptchaSolver.solveCaptcha()
    except:
        pass

    time.sleep(10)
    print(f"Time to solve the captcha: {time.time()-t0:.2f} seconds")

    # 点击按钮 (Click button)
    page('@type=submit').click()


    folder_name = 'html'
    create_folder(folder_name=folder_name)
    #Update table
    table_name = MYSQL['table']
    procedure_name = MYSQL['procedure']
    procedure_parameter = MYSQL['procedure_parameter']
    column_name = 'KEYWORD'
    status_column = 'FLAG'
    no = 2
    local_path = f'./{folder_name}/'
    s3_path = f"s3://{AWS['bucket']}/DATA/{AWS['source']}/{AWS['folder']}/"
    move_files(local_path, s3_path)

    load_driver = DriverConf()
    driver = load_driver.create_driver(page.address)

    # driver = load_driver.load_page('https://www.rp.gob.pa/LoginUsuario')
    time.sleep(3)  # Wait for the page to load completely

    time.sleep(5)
    wait = WebDriverWait(driver, 30)

    def wait_condition(button_class, text, driver):
        for _ in range(10):
            # time.sleep(3)
            # button = driver.find_element(By.XPATH, f'//button[@class="{button_class}"]')
            button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, f'//button[@class="{button_class}"]')))
            print(button.text.strip(), "== ",text)  # corrected to print buttons.text
            if button.text.strip() == text:
                return driver.page_source
            else:
                time.sleep(random.uniform(1,5))
        try:
            driver = load_driver.click_selenium_element(driver=driver, xpath='//button[@class="blazored-modal-close"]/span')
        except Exception as e:
            print(f"Exception occurred while closing the modal: {e}")
        # time.sleep(2)
        # Return None to indicate the button was not found
    #     return None

    # recaptcha_response_element = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@id = 'g-recaptcha-response']")))
    # driver.execute_script(f'arguments[0].value = "{code}";', recaptcha_response_element)
    # # recaptcha_response_element.send_keys(code)


    time.sleep(5)
    # driver = load_driver.click_selenium_element(driver=driver, xpath='//button[@type="submit"]')
    # # sys.exit()
    time.sleep(2)
    driver = load_driver.click_selenium_element(driver=driver, xpath='//a[@href="BusquedaFolios"]')
    time.sleep(2)
    for i in range(100):
        print(i)
        # time.sleep(2)
        element_gbrf = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//select[@id="tipoBusqueda"]')))
        grbf = Select(element_gbrf)
        grbf.select_by_visible_text('Mercantil')
        # time.sleep(2)
        # driver = load_driver.click_selenium_element(driver=driver, xpath='//button[contains(., "Datos de la Persona Jurídica")]')
        # time.sleep(2)
        keyword =  DbService().get_a_record(procedure_name, parameter=procedure_parameter)
        # keyword = 'gru'
        flag = False
        input_element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//input[@id="numeroFolio"]')))
        input_element.clear()
        input_element.send_keys(keyword)

        # Trigger 'blur' event to ensure the input is registered
        input_element.send_keys(Keys.TAB)

        # Alternatively, you can trigger 'change' event using JavaScript
        driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", input_element)

        # Wait for the form to register the input if necessary
        # WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.XPATH, '//input[@id="numeroFolio"]'), keyword))
        
        # time.sleep(2)
        driver = load_driver.click_selenium_element(driver=driver, xpath="//span[contains(., 'Buscar')]")
        # time.sleep(2)
        try:
            close_button = WebDriverWait(driver=driver, timeout=5).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="blazored-modal-close"]/span')))
            driver.execute_script("arguments[0].click();", close_button)
        except:
            print(traceback.print_exc())
            pass
        last_page_number = 1
        main_html = driver.page_source
        main_soup = BeautifulSoup(main_html, 'html.parser')
        page_count_span = main_soup.find('span', class_='page-link page-count d-none d-sm-block')
        if page_count_span:
            page_count_text = page_count_span.get_text(strip=True)
            # Extract the last page number from the text
            last_page_number = int(page_count_text.split()[-1])

        buttons = main_soup.find_all('button', class_='btn btn-link')

        # Get the total number of such buttons
        total_buttons = len(buttons)
        print(f"Total number of buttons found: {total_buttons}")


        for page_no in range(1,last_page_number+1):
            hit_moniter_api('panama_moniter.json')
            for i in range(1,total_buttons+1):
                try:
                    home_html = driver.page_source
                    # time.sleep(2)
                    home_tree = html.fromstring(home_html)
                    ruc_list = home_tree.xpath(f'((//tr[@class="dxbs-data-row"])[{i}]/td[@class="text-left"])[4]/text()')
                    print(ruc_list)
                    ruc = ruc_list[0]
                    roll_no_list = home_tree.xpath(f'((//tr[@class="dxbs-data-row"])[{i}]/td[@class="text-left"])[1]/text()')
                    print(roll_no_list)
                    roll_no = roll_no_list[0]
                except:
                    print("roc or folio not found or error")
                    print(traceback.print_exc())
                    continue
                
                reg_no = f'{roll_no}_{ruc}'
                print(reg_no)
                if DbService().is_value_present(check_value = reg_no):
                    print("Reg no already crawled")
                    continue
                else:
                    try:
                        driver = load_driver.click_selenium_element(driver=driver, xpath=f'(//i[@class="fa fa-eye"])[{i}]')
                        # time.sleep(3)
                    except:pass
                        
                    first_html = wait_condition(button_class='btn btn-primary', text='Datos Generales', driver=driver)
                    if first_html is None:
                        continue
                    first_html = f'<div id="DatosGenerales123">{first_html}</div>'

                    if 'Miembros Relacionados' in str(first_html):
                        driver = load_driver.click_selenium_element(driver=driver, xpath="//button[contains(., 'Miembros Relacionados')]")
                        second_html = wait_condition(button_class='btn btn-primary', text='Miembros Relacionados', driver=driver)
                        if second_html is None:
                            continue
                        
                        soup5 = BeautifulSoup(second_html, 'html.parser')
                        popup_fifth = soup5.find('div', class_='blazored-modal')
                        # time.sleep(2)
                        if 'Page 2' in str(popup_fifth):
                            print('Miembros Relacionados has page 2')
                            # time.sleep(2)
                            page_html = ''
                            pages = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="page-link"]')))
                            total_pages = len(pages)
                            for page in range(2, total_pages):
                                print(page, 2,  total_pages)
                                # insider_page = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(., '{page}')][1]")))
                                insider_page = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{page}')]")))
                                driver.execute_script("arguments[0].click();", insider_page)
                                for _ in range(5):
                                    # time.sleep(2)
                                    button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, f'//a[@class="page-link"and  @data-args="PN{page-2}"]')))
                                    print(int(button.text.strip())+1, "== ",page)  # corrected to print buttons.text
                                    if int(button.text.strip())+1 == int(page):
                                        page_html += driver.page_source
                                        break
                                    else:
                                        time.sleep(2)
                                else :
                                    flag = True
                                    break

                            if flag:
                                flag = False
                                continue

                            second_html+=page_html
                        second_html = f'<div id="MiembrosRelacionados123">{second_html}</div>'
                        first_html+=second_html    

                    with open(f'html/{reg_no}.html', mode = 'w', encoding = 'utf-8') as file :
                        file.write(first_html)
                    DbService().insert_the_record(insert_value = reg_no)

                    # time.sleep(3)
                    driver = load_driver.click_selenium_element(driver=driver, xpath='//button[@class="blazored-modal-close"]/span')
                    # time.sleep(2)
                    if last_page_number == page_no:
                        DbService().update_the_record(10, table_name, column_name, status_column, keyword, page_no, last_page_number)
                        move_files(local_path, s3_path)
                    else:
                        DbService().update_the_record(5, table_name, column_name, status_column, keyword, page_no, last_page_number)
                        driver = load_driver.click_selenium_element(driver=driver, xpath='(//li[@class="page-item dx-border-radius-inherit" and @role="presentation"]//span[@class="dxbs-pager-next"])[1]')
                        # time.sleep(3)
                        move_files(local_path, s3_path)
                
        driver = load_driver.click_selenium_element(driver=driver, xpath="//a[contains(.,  ' Limpiar todos los filtros de búsqueda')]")
except:
    print(traceback.print_exc())

finally:
    try:
        page.close()
        
    except: pass
    try:
        driver.quit()
    except:
        pass
    # Folios Madre, 
