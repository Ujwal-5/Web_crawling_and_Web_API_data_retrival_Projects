import requests
from IPython.display import HTML
from MySQLdb import _mysql
import time
import random
import sys
import traceback
import os


try:
  db=_mysql.connect("localhost","root","","crawler_db")

  flag = True
  while flag:
    try:
      db.query("CALL PROCEDURE_URL_NEVADAS(@p,@p1);")
      db.query('SELECT @p AS `SR_NO`,@p1 AS `COOKIES`') 
      r=db.store_result()
      results=r.fetch_row()
      SR_NO = results[0][0].decode()
      COOKIES = results[0][1].decode()
    
      print('SR_NO :', SR_NO, 'COOKIES :', COOKIES)
      # keyword = 10003136
      flag = False
    except Exception as e: 
      print('Empty keyword / Deadlock issue', e)
      continue  
          
  def get_company_id():
    flag1 = True
    while flag1:
      try:
        db.query("CALL PROCEDURE_URL_NEVADAS_REG(@p,@p1);")
        db.query('SELECT @p AS `SR_NO`,@p1 AS `COMPANY_ID`') 
        r=db.store_result()
        results=r.fetch_row()
        SR_NO = results[0][0].decode()
        COMPANY_ID = results[0][1].decode()
      
        print('SR_NO :', SR_NO, 'COMPANY_ID :', COMPANY_ID)
        flag1 = False
        return SR_NO, COMPANY_ID
        # keyword = 10003136
      except Exception as e: 
        print('Empty keyword / Deadlock issue', e)
        continue 


  url = "https://esos.nv.gov/EntitySearch/BusinessInformation"
  headers = {
    'Cookie': COOKIES,
    'Referer': 'https://esos.nv.gov/EntitySearch/BusinessFilingHistoryOnline',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded'
  }

  url1 = "https://esos.nv.gov/EntitySearch/BusinessFilingHistoryOnline"
  headers1 = {
    'Cookie': COOKIES,
    'Referer': 'https://esos.nv.gov/EntitySearch/BusinessInformation',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded'
  }

  url2 = "https://esos.nv.gov/EntitySearch/BusinessNameHistory"
  headers2 = {
    'Cookie': COOKIES,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Referer': 'https://esos.nv.gov/EntitySearch/BusinessInformation',
    'Content-Type': 'application/x-www-form-urlencoded'
  }

  url3 = "https://esos.nv.gov/EntitySearch/BusinessPreviousQualification"
  headers3 = {
    'Cookie': COOKIES,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://esos.nv.gov/EntitySearch/BusinessInformation',
    'Content-Type': 'application/x-www-form-urlencoded'
  }


  for _ in range(60):
    SR_NO, COMPANY_ID = get_company_id()
    payload = f'businessId={COMPANY_ID}'

    response = requests.request("POST", url, headers=headers, data=payload)
    time.sleep(2)
    response1 = requests.request("POST", url1, headers=headers1, data=payload)
    time.sleep(2)
    response2 = requests.request("POST", url2, headers=headers2, data=payload)
    time.sleep(2)
    response3 = requests.request("POST", url3, headers=headers3, data=payload)
    time.sleep(2)


    html_text = response.text + response1.text + response2.text + response3.text
    print(f"Payload ID: {COMPANY_ID}")
    

    if 'Request unsuccessful' in response.text and 'Request unsuccessful' in response1.text and 'Request unsuccessful' in response2.text and 'Request unsuccessful' in response3.text:
      print("cookie expire !!!!!")
      break


    elif 'Pardon Our Interruption' in response.text and 'Pardon Our Interruption' in response1.text and 'Pardon Our Interruption' in response2.text and 'Pardon Our Interruption' in response3.text:
      print("html data not got")
      break

    else:
       with open(f"C:\\Scripts\\Express_VPN\\HTML_FILES\\{COMPANY_ID}.html", 'w', encoding="utf-8") as file:
          file.write(html_text)
       db.query(F'UPDATE TEMP_URL_NEVADAS SET `STATUS`=10 WHERE COMPANY_ID = {COMPANY_ID}')
    time.sleep(random.uniform(1,8))
except:
  print(traceback.print_exc())
  
try:
  db.close()
except:
  pass
