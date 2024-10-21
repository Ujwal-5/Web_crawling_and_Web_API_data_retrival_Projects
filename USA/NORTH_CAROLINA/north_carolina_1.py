import requests
from MySQLdb import _mysql
import json
import subprocess
import random
import time

db = _mysql.connect("localhost","root", "", "crawler_db")      
for _ in range(50):
    time.sleep(random.uniform(1,4))
    try:
      print('fetching keyword')
      for _ in range(10):
          try:
              db.query('CALL `PROCEDURE_URL_NORTH_CAROLINA`(@p0, @p1); ')
              db.query("SELECT @p0 AS `id`, @p1 AS `keyword`;")
              break
          except Exception as e: 
              print(e)
              continue
          
      r=db.store_result()
      results=r.fetch_row()

      print(results)
      keyword = results[0][1].decode()
      print(keyword)

      url = "https://www.sosnc.gov/online_services/search/_Business_Registration_profile"

      payload = f'Id={keyword}'  #min = 4581000 max = 5073999
      headers = {
        'authority': 'www.sosnc.gov',
        'method': 'POST',
        'path': '/online_services/search/_Business_Registration_profile',
        'scheme': 'https',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Length': '10',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.sosnc.gov',
        'Referer': 'https://www.sosnc.gov/online_services/search/Business_Registration_Results',
        'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
      }

      response = requests.request("POST", url, headers=headers, data=payload)
      if "An error occurred while processing your request." not in response.text:
          url2 = 'https://www.sosnc.gov/online_services/search/_profile_filings'
          response2 = requests.request("POST", url2, headers=headers, data=payload)
          if response.status_code ==200:
            combined_data = response.text+ response2.text
            # print(combined_data)
            with open(f"{keyword}.html", 'w', encoding='utf-8') as json_file:
                json_file.write(combined_data)
            print(f"{keyword}.html is saved")
            for _ in range(5):
                try:
                    query = f"UPDATE TEMP_URL_NORTH_CAROLINA SET STATUS = 10  WHERE IN_ID = '{keyword}'"
                    db.query(query)
                    break
                except:
                    continue
          else:
            print("No data or error")
            pass
      else:
          print("No data or error")
          pass

    except:
        pass

try:
    db.close()
except:
    pass

try:
    subprocess.run(["aws", "s3", "mv", "./", "s3://dev_buk/DATA/SOURCE/NORTH_CAROLINA/HTML/", "--recursive", "--exclude", "*", "--include", "*.html"], check=True)
except: pass

