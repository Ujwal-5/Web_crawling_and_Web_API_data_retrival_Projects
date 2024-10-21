from selenium.common.exceptions import TimeoutException, WebDriverException
# from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.options import Options 
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
max_retry = 0

class DriverConf:
    def __init__(self):
        self.options = Options()
        # self.options.add_argument('--no-sandbox')
        # self.options.add_argument('--disable-gpu')
        # self.options.add_argument("--window-size=1020,900")
        # self.options.add_argument('--dns-prefetch-disable')
        # self.options.add_argument("start-maximized")
        # self.options.add_argument("--disable-popup-blocking")
        # self.options.add_argument('--disable-extensions')
        # self.options.add_argument('--disable-background-networking')
        # self.options.add_argument('--disable-background-timer-throttling')
        # self.options.add_argument('--disable-plugins')
        # # self.options.add_argument('--blink-settings=imagesEnabled=false')
        # self.options.add_argument('--enable-low-end-device-mode')
        # self.options.add_argument('--disable-notifications')
        # self.options.headless = False
        self.max_retry = 0

    def create_driver(self, listen_address):
        self.options.debugger_address = listen_address
        return webdriver.Chrome(options=self.options)

    def load_page(self, url):
        driver_conf = DriverConf()
        driver = driver_conf.create_driver()
        try:
            driver.get(url)
            return driver
        except TimeoutException or WebDriverException:
            driver.quit()

    def click_selenium_element(self, driver, xpath):
        try:
            # time.sleep(2)
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            driver.execute_script("arguments[0].click();", element)
            # time.sleep(2)
            return driver
        except TimeoutException or WebDriverException:
            if self.max_retry<3:
                self.max_retry +=1
                # driver.refresh()
                DriverConf().click_selenium_element(driver, xpath)
            else:
                print("Tried Maximum time. closing the browser")
                driver.quit()
    
    def send_key_to_selenium_element(self, driver, xpath, value, send_keys=True):
        try:
            # time.sleep(2)
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            if send_keys:
                element.send_keys(str(value))
            else:
                driver.execute_script("arguments[0].value = arguments[1]", element, str(value))
            # time.sleep(2)
            return driver
        except TimeoutException or WebDriverException:
            if self.max_retry<3:
                self.max_retry +=1
                # driver.refresh()
                DriverConf().send_key_to_selenium_element(driver, xpath)
            else:
                print("Tried Maximum time. closing the browser")
                driver.quit()

    



