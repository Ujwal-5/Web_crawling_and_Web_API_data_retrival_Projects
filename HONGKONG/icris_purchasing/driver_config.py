from selenium.common.exceptions import TimeoutException, WebDriverException
from undetected_chromedriver import Chrome, ChromeOptions
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from folder import create_folder

class DriverConf:
    def __init__(self):
        self.options = ChromeOptions()
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument("--window-size=1020,900")
        self.options.add_argument('--dns-prefetch-disable')
        self.options.add_argument("start-maximized")
        self.options.add_argument("--disable-popup-blocking")
        self.options.headless = False
        self.max_retry = 0

    def create_driver(self):
        return Chrome(options=self.options, version_main=124, use_subprocess=True)

    @staticmethod
    def load_page(url):
        driver_conf = DriverConf()
        driver = driver_conf.create_driver()
        try:
            driver.get(url)
            return driver
        except TimeoutException or WebDriverException:
            driver.quit()
            if max_retry<3:
                print("reopening the website")
                max_retry +=1
                DriverConf.load_page()
            else:
                print("Tried Maximum time. closing the browser")
                driver.quit()

    @staticmethod        
    def open_new_tab(driver, url):
        print('open in new tab')
        driver.execute_script("window.open();")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(url)
        return driver

    @staticmethod
    def click_selenium_element(driver, xpath):
        try:
            time.sleep(2)
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            driver.execute_script("arguments[0].click();", element)
            time.sleep(2)
            return driver
        except TimeoutException or WebDriverException:
            if max_retry<3:
                print("reopening the website")
                max_retry +=1
                driver.refresh()
                DriverConf().click_selenium_element(driver, xpath)
            else:
                print("Tried Maximum time. closing the browser")
                driver.quit()
    
    @staticmethod
    def send_key_to_selenium_element(driver, xpath, value, send_keys=True):
        try:
            time.sleep(2)
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            if send_keys:
                element.send_keys(value)
            else:
                driver.execute_script("arguments[0].value = arguments[1]", element, value)
            time.sleep(2)
            return driver
        except TimeoutException or WebDriverException:
            if max_retry<3:
                print("reopening the website")
                max_retry +=1
                driver.refresh()
                DriverConf().send_key_to_selenium_element(driver, xpath)
            else:
                print("Tried Maximum time. closing the browser")
                driver.quit()
    
    @staticmethod
    def take_sceenshot(driver, name, folder):
        try:
            time.sleep(2)
            create_folder(folder)
            driver.save_screenshot(f"{folder}/{name}.png")
            time.sleep(2)
            return driver
        except TimeoutException or WebDriverException:
            if max_retry<3:
                print("reopening the website")
                max_retry +=1
                driver.refresh()
                DriverConf().take_sceenshot(driver, name, folder)
            else:
                print("Tried Maximum time. closing the browser")
                driver.quit()


