from selenium import webdriver
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from MySQLdb import _mysql
import requests
from bs4 import BeautifulSoup
import re
import cloudscraper 
import sys
from IPython.display import HTML
import random
import mysql.connector
from win32com.client import Dispatch
import traceback


connection = mysql.connector.connect(host="localhost",user="root",passwd="",database="crawler_db")

def get_keywords():
        for _ in range(10):
            try:
                cursor = connection.cursor()
                cursor.execute("CALL PROCEDURE_KEYWORDS_2_MASSACHUSETTS(@p,@p1);")
                cursor.execute('SELECT @p AS `SR_NO`,@p1 AS `KEYWORD`') 

                output_params = cursor.fetchone()
                keyword = output_params[1]
                print('keyword :', keyword)
                cursor.close()
                return keyword
                break
                
            except Exception as e:
                print('Empty keyword / Deadlock issue', e)
                print(traceback.print_exc())
                continue 
        
keyword = get_keywords()

def get_sysvalue():
    for _ in range(10):
        try:
            cursor = connection.cursor()
            cursor.execute("CALL PROCEDURE_URL_MASSACHUSETTS_range(@p,@p1)")
            cursor.execute('SELECT @P AS `SR_NO` ,@P1 AS `FilingId`')
            OUTPUT_PARAMS = cursor.fetchone()
            filingid = OUTPUT_PARAMS[1]
            cursor.close()
            return filingid
            break
        
        except Exception as e:
            print("error might be in PROCEDURE_URL_MASSACHUSETTS_range")
            print(traceback.print_exc())
            continue

max_retry = 3
def click_with_retry(element):
    retry = 0 
    while retry < max_retry:
        try:
            time.sleep(random.uniform(1,5))
            # driver.execute_script("argument[0].click();", element)
            element.click()
            return True
        
        except Exception as e:
            retry += 1
            print(f"Click failed. Retrying... ({retry}/{max_retry})")
            time.sleep(random.uniform(1, 3))



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
options = ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
# options.add_argument('--headless=new')
options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"')
options.headless = False

driver = Chrome(options=options, version_main=major_version)

try:
    driver.get('https://corp.sec.state.ma.us/corpweb/corpsearch/CorpSearch.aspx')
    wait = WebDriverWait(driver, 30)

    Entity_name = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '//tr[@class="RowHeight36"]/td[@style="width: 47%"]/input[@class="p3"]')))
    Entity_name.send_keys(keyword)
    time.sleep(random.uniform(1,4))

    search_type = wait.until(EC.element_to_be_clickable((By.XPATH,'//select[@name="ctl00$MainContent$ddBeginsWithEntityName"]')))
    click_with_retry(search_type)
    type_option = wait.until(EC.element_to_be_clickable((By.XPATH,'//select[@name="ctl00$MainContent$ddBeginsWithEntityName"]/option[@value="B"]')))
    click_with_retry(type_option)


    no_of_items = wait.until(EC.element_to_be_clickable((By.XPATH,'//select[@name="ctl00$MainContent$ddRecordsPerPage"]')))
    click_with_retry(no_of_items)
    items_option = wait.until(EC.element_to_be_clickable((By.XPATH,'//select[@name="ctl00$MainContent$ddRecordsPerPage"]/option[@value="All items"]')))
    click_with_retry(items_option)


    search_corporations = wait.until(EC.element_to_be_clickable((By.XPATH,'//input[@name="ctl00$MainContent$btnSearch"]')))
    search_corporations.click()
    time.sleep(random.uniform(1,3))
    driver.refresh()


    cookies = driver.get_cookies()
    cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    print(cookie_string)
    time.sleep(random.uniform(1,4))
    driver.close()

except Exception as e:
    print("error found in selenium")
    print(traceback.print_exc())


if cookie_string =="":
    sys.exit()

scraper = cloudscraper.create_scraper()
url = "https://corp.sec.state.ma.us/CorpWeb/CorpSearch/CorpSearchResults.aspx"

payload = {}
headers = {
'scheme': 'https',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en-US,en;q=0.9',
'Cache-Control': 'max-age=0',
'Cookie': cookie_string,
#'visid_incap_2224066=tehFKdcuSHGYyhmb8TD7LptBoWUAAAAAQUIPAAAAAABUwCG9As9HXF/EPvT2ObLE; visid_incap_2233578=mCWzkn9yQeSsOb28B7A6zkVNoWUAAAAAQUIPAAAAAAAxBPVIkHGLKuTtAMen3H5d; ASP.NET_SessionId=r5qujqe0dwgeffyqklovgnve; nlbi_2224066=ZAr1LqV322QOqIowH0WRZAAAAADWAp7agRAx1uFfPKYcFoHU; incap_ses_7223_2224066=iIPFdFRxaiFAulfaTUE9ZMMaumUAAAAApeAfpdoom2doNRAuRpB67Q==; incap_ses_1362_2224066=HlGIBWAVtFakjLtp1MzmEuUeumUAAAAA7xJfMFTM3O2mzmfBUIn8bQ==; incap_ses_1338_2224066=jSbvff5+LzCcCPSm64iREsUhumUAAAAASGYFatQ8ZWN9H4+HM1ArWQ==; incap_ses_358_2224066=HcJQHB8xSlDsKhjFHN/3BFMiumUAAAAA7Su/Mtq693qmH+G8gFZkDg==; incap_ses_1457_2224066=W/PBaELMjmcGbMFemU44FEYoumUAAAAA7vcHYXNJYvXvyGX9/OrU4Q==; incap_ses_5030_2224066=LlKVS7qoZVYwe8R6iibORQMyumUAAAAAUboob/Tw7w5LOoP+F6PB/A==; incap_ses_703_2224066=GsJTKOSATGOhi1k054/BCfJJumUAAAAADClLLa4tVSEYaPGPq0SZLw==; incap_ses_220_2224066=c+xaVGJTOSJEYDpNBJoNA/5JumUAAAAAksD2m5yaL8G1V+mD0u2NOw==; incap_ses_1316_2224066=S1MJHhZQDDUuFVx+CWBDEglKumUAAAAAgUD6cGgUQx5kaxC6d86PTg==; incap_ses_5031_2224066=MXDTYss1BB4/tfZzC7TRRRxKumUAAAAATbduWxAYdIFa66tqPyaA4w==; incap_ses_5033_2224066=9cQbDcZ6y2jBJhoSC8/YRShKumUAAAAA/ovHHP8y84pQ/HrhGmi/2Q==; nlbi_2224066_2147483392=Nc2KUPrGcVdiZp7gH0WRZAAAAAA83J1fDcoe79sUVxMVHurm; reese84=3:7lTWnzauGp8I9IsWvochrg==:NhJlX3mVsumdkZMaMkKpSU0jClY+G1xSoW75atsJnRD8jjTdonjI1veS7Vfqhu15ix1QLlHhOPIyAfeg0Oh8B4cAQbymu0ORm0PJxqD9tbfkRaF7YNGpmDcIDfHNh4JBffj4dTR6+s6etIqfQa0G1rRTkiziBPJT4hDnNiP1wu5jEfix52R5jVOAXVpmI57sEfFjxkligVCJX/CgzQZJobSaKtx4qSGcogKOWSxTUsqPtbhJKJXJK3/j16ZbRHHnmRCc5Plc2Z7Inr2fP/nCPGVGAEpAodDuj8Uu055Gef3S8PiyDK3zA2EC+QM7BmA7/UegHX3sm3k2SsnUvRvKIg5Jh+c1dBzRHmAXc76oLXspcvnvMptVkLsm85QOOqpwY3G5kvHhIMPlwhWpVk6yqePC9xFEHbg1W6HXz92ZfHKw7g1UKEsgYdUexatnhMB0OuB65Lxuh9gtpw2C9SjeBlY729m0ISdxpD1nrgLMhHc=:/6uNL+3LgYdGNddJGFBrtKhEUdEk9JAG+H6/O3jpzkU=; incap_ses_1316_2224066=13fpEdwQhz6BcgN+CWBDEocnumUAAAAAYqjHxAnVOZ9AbF1qy6ZYMQ==; incap_ses_1338_2224066=MtKxIumVZXRT5j6n64iREudKumUAAAAAyMa5nuCn2dRoB09lOatf5w==; incap_ses_1362_2224066=CHGvSy78R3mgusZp1MzmEmwnumUAAAAAgRNcK7EylPhHwKjt8F+KxQ==; incap_ses_1451_2224066=DHzdYWQrJncdv8N1tv0iFKRNumUAAAAAxdzJqj8zwk19ZWBkYobj6w==; incap_ses_1457_2224066=XwTSTAuHyD85jO9emU44FDNLumUAAAAAge/Hd+upD0AGZhcsPJjhPQ==; incap_ses_1460_2224066=0vfUSMITLhYBDgL5EvdCFDpOumUAAAAAHjKjsU2jM28zHtHLHMfcXA==; incap_ses_1463_2224066=BLAWO4fKCQYSRkvsgJ9NFDtLumUAAAAAtssKWwWg0/+u0A3PgaYF0A==; incap_ses_220_2224066=c/6dP5mLYivXoDtNBJoNA75KumUAAAAANX2nPscS2OGG7rGCke3lnQ==; incap_ses_221_2224066=Cpxlblv4dj78G7JTaScRA6lNumUAAAAAoZqZTwRZKM3YZ157eWoSnw==; incap_ses_356_2224066=ko4EGFp6KxvnoU3Nmc/wBJAnumUAAAAABe/UhL0fq41HfKekmPorng==; incap_ses_488_2224066=SuqbU6KF1nLKBDe3u7rFBldLumUAAAAAvztDZ+zh8lm+NxsHELqQaw==; incap_ses_5030_2224066=Xht8ARpMw3gEgdt6iibORcZNumUAAAAAL6TbO84rI8qwn/djO34Cww==; incap_ses_5031_2224066=gOlMBaV0FGcHTsBzC7TRRacfumUAAAAAbTPNTMC37d9lc/cLpEYNNA==; incap_ses_5032_2224066=uT0IfoxSvD8DqGbCjkHVRVBLumUAAAAA4/WksqRtV1/cdXWEH110vQ==; incap_ses_5033_2224066=B4ACNDcuzEK6VxwSC8/YRWZLumUAAAAAuh4xB08eCNlfR3t82QKDcA==; incap_ses_701_2224066=Y44bJvdJZhnT0VEfK3W6Ce9NumUAAAAAiOm748X1s6TNPwD4WenPtA==; incap_ses_703_2224066=dB/cLE9HuGInNjI054/BCXonumUAAAAAe1RqKuochY4mQBYYM+UBDg==; incap_ses_7223_2224066=aaA4F1aex1DBSpTaTUE9ZMtNumUAAAAAvGpOlX268R0cfmeHsVdXTA==; incap_ses_7225_2224066=n6ozNNfU6ApSvxU0NlxEZIsnumUAAAAAlGqSM58KLAL0Th17yLbTwA==; visid_incap_2224066=Y54m8VMoRemgJ0kTKUNNBN2np2UAAAAAQUIPAAAAAABoXPgJROQ0JJL+NJWsBm1d; incap_sh_2224066=QE66ZQAAAACAmnIJBgAQwJzprQaaFDrx1Lc8oX+eCrNvL+aI',
'Referer': 'https://corp.sec.state.ma.us/CorpWeb/CorpSearch/CorpSearch.aspx',
'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
'Sec-Ch-Ua-Platform': '"Android"',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36'
}


response = scraper.post(url, headers=headers, data=payload)

html_text = response.text

soup = BeautifulSoup(html_text,'html.parser')
sysvalue_list = [
re.search(r'sysvalue=([^&\']*)', a['href']).group(1)
for a in soup.find_all('a', class_='link', href=re.compile(r'sysvalue='))
]
print('sysvalue_list', sysvalue_list)

if sysvalue_list:
        cursor = connection.cursor()
        print('insert list', sysvalue_list)
        placeholder = ', '.join(['%s'] * len(sysvalue_list))  # Assuming each sublist has one element
        query = f"INSERT IGNORE INTO `URL_MASSACHUSETTS` (FilingId) VALUES (%s)"
        print(query)
        sysvalue_list = [(item,) for item in sysvalue_list]
        print(sysvalue_list)
        try:
            # Execute the query for multiple records
            cursor.executemany(query, sysvalue_list)
            connection.commit()
        except Exception as e:
            print("Error:", e)
            connection.rollback()
        finally:
            cursor.close()
  

for _ in range(3):
    filingid = get_sysvalue()
    url_1 = f'https://corp.sec.state.ma.us/CorpWeb/CorpSearch/CorpSummary.aspx?sysvalue={filingid}'

    headers_1 = {
        'Cookie': cookie_string,
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36'
    }

    try:
        time.sleep(random.uniform(2,8))
        response_1 = scraper.post(url_1, headers=headers_1)
        html_content =response_1.text

        if 'Request unsuccessful' in html_content:
            print("cookie expire !!!!!")
            break

        soup = BeautifulSoup(html_content, 'html.parser')
        find_element = soup.find('td', class_='p5')
        if find_element:
            inner_span = find_element.find('span', class_='p5') 
            if inner_span:
                text_content = inner_span.text  
            else:
                text_content = "Not Found"
        else:
            text_content = "Not Found"

        print(text_content)

        viewstate = soup.find('input', {'id': '__VIEWSTATE'})['value']
        viewstate_generator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
        event_validation = soup.find('input', {'id': '__EVENTVALIDATION'})['value']

        print('filingid....................................................................',filingid)
        

        url_2 = f"https://corp.sec.state.ma.us/CorpWeb/CorpSearch/CorpSearchFormList.aspx?sysvalue={filingid}"

        payload_2 = {'__EVENTTARGET':'',
        '__EVENTARGUMENT':'',
        '__VIEWSTATE': viewstate,#'/wEPDwULLTE5OTI2NDgzNjMPFhAeA1VBQWQeBEZFSU4FCTA0MzU4MjEyNh4LU0VBUkNIX1RZUEUFATEeDkVudGl0eVR5cGVDb2RlBQQwMjAwHgNDSUQFBkNUMkZXNh4ORW50aXR5VHlwZURlc2MFG0RvbWVzdGljIFByb2ZpdCBDb3Jwb3JhdGlvbh4KQWN0aXZlRmxhZwUBTh4LQ09SUF9TRUFSQ0gyhxcAAQAAAP////8BAAAAAAAAAAwCAAAAP0NvcnBDb3JlLCBWZXJzaW9uPTEuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49bnVsbAQBAAAAjQFTeXN0ZW0uQ29sbGVjdGlvbnMuR2VuZXJpYy5MaXN0YDFbW0NvcnBXZWIuQ29ycENvcmUuTW9kZWwuU2VhcmNoUmVzdWx0QmFzZSwgQ29ycENvcmUsIFZlcnNpb249MS4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1udWxsXV0DAAAABl9pdGVtcwVfc2l6ZQhfdmVyc2lvbgQAAClDb3JwV2ViLkNvcnBDb3JlLk1vZGVsLlNlYXJjaFJlc3VsdEJhc2VbXQIAAAAICAkDAAAAGQAAABkAAAAHAwAAAAABAAAAIAAAAAQnQ29ycFdlYi5Db3JwQ29yZS5Nb2RlbC5TZWFyY2hSZXN1bHRCYXNlAgAAAAkEAAAACQUAAAAJBgAAAAkHAAAACQgAAAAJCQAAAAkKAAAACQsAAAAJDAAAAAkNAAAACQ4AAAAJDwAAAAkQAAAACREAAAAJEgAAAAkTAAAACRQAAAAJFQAAAAkWAAAACRcAAAAJGAAAAAkZAAAACRoAAAAJGwAAAAkcAAAADQcFBAAAACJDb3JwV2ViLkNvcnBDb3JlLk1vZGVsLkNvcnBGaWxpbmdzFAAAAAtfRmlsaW5nQ29kZRVfRW50aXR5VHlwZURlc2NyaXB0b3ILX0ZpbGluZ05hbWULX0VudGl0eU5hbWUQX05ld0NvcnBSZWZpbGluZxZfRW50aXR5VHlwZUNvZGVEaXNwbGF5Bl9TdGFnZQpfQWdlbnROYW1lDl9SZXNpZGVudEFnZW50B19TdGF0dXMJX0ZpbGVZZWFyCV9EZXRhaWxJRAtfU3RhdHVzRmxhZw9fRmls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FgIfCAUCwqBkZAICDw8WAh8KaGRkAj8PZBYCZg9kFgJmD2QWAgIBDxBkZBYAZAJDD2QWAgIBD2QWAmYPZBYCAgEPEA8WBh4NRGF0YVRleHRGaWVsZAULTGlzdEJveFRleHQeDkRhdGFWYWx1ZUZpZWxkBQxMaXN0Qm94VmFsdWUfDGdkEBUZC0FMTCBGSUxJTkdTDUFubnVhbCBSZXBvcnQXQXBwbGljYXRpb24gRm9yIFJldml2YWwVQXJ0aWNsZXMgb2YgQW1lbmRtZW50HUFydGljbGVzIG9mIENoYXJ0ZXIgU3VycmVuZGVyMUFydGljbGVzIG9mIENvbnNvbGlkYXRpb24gLSBEb21lc3RpYyBhbmQgRG9tZXN0aWMwQXJ0aWNsZXMgb2YgQ29uc29saWRhdGlvbiAtIERvbWVzdGljIGFuZCBGb3JlaWduFkFydGljbGVzIG9mIENvcnJlY3Rpb24ZQXJ0aWNsZXMgb2YgRG9tZXN0aWNhdGlvbh1BcnRpY2xlcyBvZiBFbnRpdHkgQ29udmVyc2lvbipBcnRpY2xlcyBvZiBNZXJnZXIgLSBEb21lc3RpYyBhbmQgRG9tZXN0aWMpQXJ0aWNsZXMgb2YgTWVyZ2VyIC0gRG9tZXN0aWMgYW5kIEZvcmVpZ24YQXJ0aWNsZXMgb2YgT3JnYW5pemF0aW9uGkFydGljbGVzIG9mIFNoYXJlIEV4Y2hhbmdlIUFydGljbGVzIG9mIFZvbHVudGFyeSBEaXNzb2x1dGlvbmRBcnRpY2xlcyBvZiBWb2x1bnRhcnkgRGlzc29sdXRpb24gb2YgQ29ycG9yYXRpb24gV2hpY2ggSGFzbid0IElzc2VkIFNoYXJlcy9IYXNuJ3QgQ29tbWVuY2VkIEJ1c2luZXNzPENlcnRpZmljYXRlIG9mIENoYW5nZSBvZiBEaXJlY3RvcnMgb3IgT2ZmaWNlcnMgKFJlc2lnbmF0aW9uKTJSZWluc3RhdGVtZW50IEZvbGxvd2luZyBBZG1pbmlzdHJhdGl2ZSBEaXNzb2x1dGlvbiFSZXN0YXRlZCBBcnRpY2xlcyBvZiBPcmdhbml6YXRpb24ZUmV2b2NhdGlvbiBvZiBEaXNzb2x1dGlvbi1TdGF0ZW1lbnQgb2YgQXBwb2ludG1lbnQgb2YgUmVnaXN0ZXJlZCBBZ2VudCA5U3RhdGVtZW50IG9mIENoYW5nZSBvZiBSZWdpc3RlcmVkIEFnZW50L1JlZ2lzdGVyZWQgT2ZmaWNlRFN0YXRlbWVudCBvZiBDaGFuZ2Ugb2YgUmVnaXN0ZXJlZCBPZmZpY2UgQWRkcmVzcyBieSBSZWdpc3RlcmVkIEFnZW50MFN0YXRlbWVudCBvZiBDaGFuZ2Ugb2YgU3VwcGxlbWVudGFsIEluZm9ybWF0aW9uICxTdGF0ZW1lbnQgb2YgUmVzaWduYXRpb24gb2YgUmVnaXN0ZXJlZCBBZ2VudBUZBzAwMDAwMDAHMDIwMDAwNAcwMjAwMDA2BzAyMDAwMDcHMDIwMDA1MQcwMjAwMDA4BzAyMDAxODIHMDIwMDA3OQcwMjAwMDUwBzAyMDAwNTUHMDIwMDAwOQcwMjAwMTgwBzAyMDAwMTMHMDIwMDA2MgcwMjAwMDEwBzAyMDAwNjQHMDIwMDAxOQcwMjAwMDY4BzAyMDAwNDEHMDIwMDA2NwcwMjAwMDc1BzAyMDAwNzYHMDIwMDA3NwcwMjAwMDc0BzAyMDAwNzgUKwMZZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZxYBZmQCRQ9kFgICAQ9kFgJmD2QWAgIBDw8WAh8IZWRkGAgFHWN0bDAwJE1haW5Db250ZW50JGdyZFRydXN0ZWVzDzwrAAwBCAIBZAUbY3RsMDAkTWFpbkNvbnRlbnQkZ3JkU3RvY2tzDzwrAAwBCAIBZAUdY3RsMDAkTWFpbkNvbnRlbnQkZ3JkUGFydG5lcnMPPCsADAEIAgFkBR1jdGwwMCRNYWluQ29udGVudCRncmRNYW5hZ2Vycw88KwAMAQgCAWQFImN0bDAwJE1haW5Db250ZW50JGdyZE90aGVyTWFuYWdlcnMPPCsADAEIAgFkBR1jdGwwMCRNYWluQ29udGVudCRncmRPZmZpY2Vycw88KwAMAQgCAWQFHGN0bDAwJE1haW5Db250ZW50JGdyZFBlcnNvbnMPPCsADAEIAgFkBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBAUhY3RsMDAkTWFpbkNvbnRlbnQkbHN0Q2hlY2tCb3hlcyQwBSFjdGwwMCRNYWluQ29udGVudCRsc3RDaGVja0JveGVzJDEFIWN0bDAwJE1haW5Db250ZW50JGxzdENoZWNrQm94ZXMkMgUhY3RsMDAkTWFpbkNvbnRlbnQkbHN0Q2hlY2tCb3hlcyQzjgZTsDotheMhYAA7XXftEWQbzPY/nFsbuf7CoXT5SeA=',
        '__VIEWSTATEGENERATOR': viewstate_generator,#'F5CB3FBE',
        '__EVENTVALIDATION': event_validation,#'/wEdACQ4g1LRVkRzpCrswLKBRVIx3WFT+Ibe4cn+oOIFwZVE1mhCSllrinsmw89j4zE5Ajz8ZIrLJ6Qs2zRP1cTP41ZTPnGY1Jfq6/KP4SyUOj8vHy8L7U8z7leiV01Vrh+tgAWTKO7FoAqdXMwZBbdwHWK1/jv2xGtu4Z4xTIYcCTjnPoJYhzAaQysj8WV5lg2E1ibgay5/sblgRaDjNy5HsBcFxKK0dLImGYPJS8xFjYBKO53geuZ6nCrmw17R/5Wg0RJKsFWuzmyq1lNyeQuyaDauch8Fg4SjB/0NCEJQjvN+szGlM2R51+IjKlOA+Li3WJeYUTET8jXrPJoSvDmFBoqMImGLPHDD2Y/KVksMiAGz2PtrUNvAHN0JBAFl89pPh4yBLibRX6SuQYwfBZcV1RbTFkn1hXjlP66YcSiQ5dFYDuJ8R760Dh+CJEoGcl3X5crnjmxsa5pnsThu47yA4eA3Lec/b79oJpnnVa0mdxZgNKOWjnURYxiRXQNjlQlYe793IqT6UgMMqDYjZQ2hUAqKRGFjzMoG7gccVr+GAE24ArcQBImOaXXcs6ErEwOk21MdSJZWwDeeybAhhSAdWTlkrEik1x7VEZyHfAZ50j4wJ257ME5nzVGnXkHyodERWWRFbQVa33sxYE6T2dmrO1Vimya/1HqQF133h7vBmLQNpLXlVdszsAKRAwwxaizGlbtk2kWDBbAD8IgWOTWEZTL7x2brtjzsjo4mdzvj3Ti3N4ZZKE/WyFQK4nI3/4Z3rSpUUq6Z6scgjX0YYvdF77szDecJwARPiozKcRFKUQdbuA==',
        'ctl00$MainContent$btnViewFilings':'View filings',
        'ctl00$MainContent$txtComments': ''}
        

        headers_2 = {
        'authority': 'corp.sec.state.ma.us',
        'method': 'POST',
        'path': f'/CorpWeb/CorpSearch/CorpSummary.aspx?sysvalue={filingid}',
        # 'scheme': 'https',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        # 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        # 'Cache-Control': 'max-age=0',
        # 'Content-Length': '12080',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie_string,#'visid_incap_2224066=cY+XprwNQyKd6AX0qLqa9CDIxWUAAAAAQUIPAAAAAABERjOnbuoLwHOXMTo/641s; ASP.NET_SessionId=raxvt3nnx555rdfg55mwnxub; nlbi_2224066=p8KRRIyiExwmNmLxH0WRZAAAAADzzp67zvCGfV8f4j4X/V4x; incap_ses_524_2224066=kANXJMPKeWp2hWKbSZ9FB9NnJ2YAAAAAhAGtcCU4XqLXsz1IAN+Zmg==; incap_ses_227_2224066=1bcvSLlyZjVZp84jU3cmA/JnJ2YAAAAAW9VcJSY/7n7Pb2jWkc862g==; incap_ses_996_2224066=eWofAeVOIRlMfobGvYDSDRpoJ2YAAAAAnkiI2jDVGDFW3WQhpO9N9Q==; incap_ses_1599_2224066=GpcHSSqMhhLgNj/kC8owFnBoJ2YAAAAAcAIsccjVPH+ElluwWAlPKg==; incap_ses_237_2224066=qE6pEbva8G0KJa6ZRf5JA2tuJ2YAAAAAZiYi/FOVfYEwYWW+5Y8bWw==; incap_ses_5031_2224066=tcWbNgKc0RjOhojo3LPRRZ9uJ2YAAAAALKmgxevGje9qjaRBlD/JRQ==; incap_ses_480_2224066=8nvrQvrYvHCe1bL4gk2pBt5uJ2YAAAAAI/mvNbOc2FUf9LAen46PBw==; incap_ses_1316_2224066=bxDkHfDIU0vNqsm7C19DEh9vJ2YAAAAATKkeayXCP8H8HKGHcVXhnA==; incap_ses_890_2224066=D5p8GWLyoWlPkfvnT+pZDLRvJ2YAAAAAdv4XEWinI2f3iE6tSrT6uQ==; incap_ses_1547_2224066=9Jt/FFotKRxbBcJ6Ugx4FcRvJ2YAAAAAqZ0TZCKRtEBhSGqpk3KJog==; incap_ses_1405_2224066=r3L8TES+00f+7lhYFZB/E/R0J2YAAAAAcZa1dHCuOTGIIerF/ctp0Q==; incap_ses_685_2224066=pKHPHB+exXrYNzKQ45uBCUd7J2YAAAAA2x1feIEo65/MiMbuoIBeKA==; incap_ses_419_2224066=lB/bOcxmRCpQURKuTpbQBXN8J2YAAAAA2mdi2FsUPVTw4nFp8xmnTA==; incap_ses_327_2224066=a0xpA5qf/ArexKzKzbyJBK58J2YAAAAANMBAjo6jHliJaLDpjrmLGA==; incap_ses_195_2224066=8Lm7OB9JsgTI41MxfMe0AnuAJ2YAAAAAv3M5h8+1BoUUMAu3Us8Fug==; incap_ses_205_2224066=LIrdQUyoCBiHsnmibk7YAriAJ2YAAAAAHw2koYP79n6VsRoSn5NGiQ==; incap_ses_202_2224066=S7SPZjXSlFQ/H4yy8qXNAsWGJ2YAAAAAC/QYfrxzEhy+CRXlzeoMfA==; incap_ses_1412_2224066=w5ckXKOv1QgWKROCiW6YEzyHJ2YAAAAAWESgIalXlYTdQ9QVEeC/xw==; incap_ses_1327_2224066=Z8XhbrXxa1iAaUNygXNqErOHJ2YAAAAAOYexxYLsSvQsvNaovbo8yA==; incap_ses_418_2224066=nCM3ZWALUFbZA+7AzQjNBReNJ2YAAAAAHdndlSHG4LSoxqfQuA22qQ==; incap_ses_261_2224066=ovAqK9fzpQGby1QGJUKfA4+NJ2YAAAAAcWZwD6I9zEuAieZ43qZFlg==; incap_ses_7232_2224066=KTUlbB+RIh6EmzKbszldZLuOJ2YAAAAAopLg0VIsgc3IRhYzDfZmcA==; incap_ses_1558_2224066=cR9vAlYCfTNc9zuHwyCfFZaUJ2YAAAAAAIdKZLjTPb2whK4yTTqUww==; incap_ses_415_2224066=zoFGfRdzjxSs5aV7VmDCBe+WJ2YAAAAAuWPXHiV/JZ0F/56LRSmR7Q==; incap_ses_725_2224066=PZqUP/XH1Rtt8q7/sbcPCuyaJ2YAAAAAg8E5R9R2AG4f4p4kFiwwLg==; incap_ses_2109_2224066=wSFNPJzKujT5RHdHWKxEHZ+bJ2YAAAAACfxEH/kOnY+Gc9J7X4UtQw==; incap_ses_1606_2224066=Njo7cY9YZEQlUkgPgKhJFrudJ2YAAAAApUegmEyQCSars7dZWugVuQ==; incap_ses_9219_2224066=CQCPLfcR9kpHZAGKrHfwf/aeJ2YAAAAAh3Sv9u55vP61t91ovob30g==; incap_ses_1598_2224066=PavVLf6W2BRR1gpAjTwtFgWfJ2YAAAAAvuR0Xse0YbvkNd6xjQk3pw==; incap_ses_1244_2224066=npImQXqWD3+3weS3b5NDETahJ2YAAAAATwbMoZFU99Xu2xWHf77kCg==; incap_ses_1551_2224066=vxj2ZcjP4HWuK2X+TEKGFXShJ2YAAAAAQMFKJcxUUud1UQiMtRJxGQ==; incap_ses_1532_2224066=1NsLAQ76ZwUcOQTB5sFCFXqhJ2YAAAAAbvo+umCyuyMZAVciyAG/5A==; incap_ses_239_2224066=KULLQDgSG0yJJ4fXQhlRA4ahJ2YAAAAAgQTtnxTMw0fzPRD/7H+fpw==; incap_ses_440_2224066=QOt6dNXUJgHSbe3btjEbBqGiJ2YAAAAAadIXz1xnd8zw53HNf5xebg==; incap_ses_385_2224066=suBaLVZL7mimZvAif8tXBbWiJ2YAAAAAb0zr4dM9IVYTROqiSlW1pg==; incap_ses_1814_2224066=FCvvTKyHfVSH7H5VaJ8sGcOiJ2YAAAAA4LBasKmP38HGpvTbRqskjw==; incap_ses_1815_2224066=lgLmW6vG/jF2sBL35iwwGZejJ2YAAAAAJg5Na4XJJQ7zHPw5cavDog==; nlbi_2224066_2147483392=XJwPMrDmKHtfWX1dH0WRZAAAAAANc+STx0+nWHhuf1CDHS66; incap_ses_1533_2224066=7AyEQRX3MSuDbkBpZU9GFcakJ2YAAAAApCXG+YTAKlYpk2EUYwyywQ==; reese84=3:CLmuM83oRa6RqP2lBORjRg==:rFw6V9ucDaSU7haYmm/2oysWwtExU70Xe7WbBRLvNfhdXPgPcfzCq7T/qKl5f4hHjrlyfktIK+9HNNUtXswup4IbWmBk9ckE/BGP6Rja+UXYgXEbSEalCUrfL57FMgDfReX4BECC6r9iHltBc0Rw2UTqN1ZC2qF9YJZo7R/s4zjmmz3bOzu9r/xNhv+h/BGGzcQtiWbhb2RZ1pu3ya5//ls+TJpfRJI09m5p5DYjUSl8wTIS0q/MaA3oH3soUmJvTJ7Gxgm35y2bCglXgmbAjmA7bXLvEB2LdIRqphNXqeKKvpwMyFCn+Hj6ROToQmyMq6wRSKe/8zxoYRSIG70vbx9H6PBb8iFjmpzapOvgYU5h9B6rLPBbUb2Z8WuQOTwmEzRrd+a7ZLDzxlkrCgFWkzuyVHv0stff0WAwrrEwFPYXcjly08DWYNVXd6Fgn7qmHjwSrkOqQ/bBobDvEqfiQg==:tLuH+TaxETEVBHxh2OnMsnVJHwBFIBf8EYIz+1jju+4=; incap_ses_1436_2224066=GfxwPTw+hUWOd+v0aLLtEzWBJ2YAAAAAxPjO85bauOUEopWv5+Eq4Q==; incap_ses_1457_2224066=eWbeaOqAf1BkiRV7zE04FLRsJ2YAAAAAyL0E4ORcO+Wj9sosVTAyeA==; incap_ses_153_2224066=QL35YzwclCMMoJ97t5AfAqSoJ2YAAAAAPJWuKTHXxYc/qk6i3cAwcQ==; incap_ses_1548_2224066=mjJHU8wOHWHFv3kW0Zl7FSxsJ2YAAAAADcKL8rIs9vZV3KSkRgpE8Q==; incap_ses_1558_2224066=Zcu0DpAfPTgKBFSHwyCfFXyqJ2YAAAAAQTCu/OdNUFHMJFNvpy8yNA==; incap_ses_157_2224066=6LrdUXv1KytQUnJgtMYtAl1kJmYAAAAABCv9HW5IMGPDWUsQ2zHM0Q==; incap_ses_159_2224066=2CzgMZzXGRd+RGerseE0Ao6oJ2YAAAAApahiErjNSl6qOB5sDv371g==; incap_ses_161_2224066=7d64H5h68U8k05T1rvw7AvSlJ2YAAAAACvWEcfwgJBy0HoWuofOJUQ==; incap_ses_180_2224066=oZ2WaJ9DxBgnGUjcEn1/AraoJ2YAAAAAMQvrZlKWs6fxpSgPDBu9mQ==; incap_ses_181_2224066=ULD+corBXnuUQYDTkwqDAqmrJ2YAAAAAqtOBWHMhi/1LTaIrKevgHA==; incap_ses_182_2224066=6B1iR0Qy8kfJkAt6EpiGAtmsJ2YAAAAA61peM3QDdXwfzLJUTV4Bdg==; incap_ses_185_2224066=TGLFLCVu2gsTglASjECRAkxkJmYAAAAA2x6MFsJk8QHlP1H0Ug8LJg==; incap_ses_216_2224066=Kp7hKJLpvygKhJkH4mL/AkCrJ2YAAAAAIcpTPJkI23GGCKPZgcA5jw==; incap_ses_230_2224066=xqbBUZ047VFFvB1f0R8xA66mJ2YAAAAA3bmjSz/0KGaNp0G4yzCWkQ==; incap_ses_270_2224066=LndoHNy8qQV7yxl1lju/A3ioJ2YAAAAA+JrgJmx7F1Z9VsfKio9Wbw==; incap_ses_278_2224066=ZzPbQiHK4EQr6wmbi6fbA+ulJ2YAAAAAuNgSSKwm4ovYVsNgCWW+eg==; incap_ses_358_2224066=yINbGIRhDBDNLA1mKN/3BJlvJ2YAAAAAPx6DEsw9D6VFxT7aqcIiWA==; incap_ses_5032_2224066=OySLCNzsHiutYK6MW0HVRb1sJ2YAAAAAzAUzlmMOZVGNoW3Ht6waYg==; incap_ses_888_2224066=1NP4Z1OTRmmV2RCmUs9SDCVwJ2YAAAAACTP1R4OYlybSFl0g050dKg==; incap_ses_9219_2224066=4rLFUwRP4SAm5OyJrHfwfzlrJ2YAAAAAP3rM4FKl8RtfGNCC6gZ2hg==; visid_incap_2224066=Y54m8VMoRemgJ0kTKUNNBN2np2UAAAAAQUIPAAAAAABoXPgJROQ0JJL+NJWsBm1d',
        'Origin': 'https://corp.sec.state.ma.us',
        'Referer': f'https://corp.sec.state.ma.us/CorpWeb/CorpSearch/CorpSummary.aspx?sysvalue={filingid}',
        # 'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        # 'Sec-Ch-Ua-Mobile': '?0',
        # 'Sec-Ch-Ua-Platform': '"Windows"',
        # 'Sec-Fetch-Dest': 'document',
        # 'Sec-Fetch-Mode': 'navigate',
        # 'Sec-Fetch-Site': 'same-origin',
        # 'Sec-Fetch-User': '?1',
        # 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }

        response_2 = requests.post(url_2, headers=headers_2, data=payload_2)

        print(response_2.text)
        full_html = html_content + response_2.text



        with open(f'HTML/{text_content}.html', 'w', encoding="utf-8") as file:
            file.write(full_html)
            print(f"{text_content}.html download successfully")

    except Exception as e:
        print(traceback.print_exc())


    