from twocaptcha import TwoCaptcha
import os
import json
import requests
from bs4 import BeautifulSoup
import time
import random
from requests.exceptions import RequestException
from MySQLdb import _mysql
from moniter import hit_moniter_api
import subprocess

def make_request_with_retry(url, headers, data, max_retries, retry_delay):
    for attempt in range(max_retries):
        time.sleep(random.uniform(1,5))
        try:
            response = session.post(url, headers=headers, data=data)
            response.raise_for_status()  # Raise an error for non-2xx status codes
            return response
        except RequestException as e:
            print(f"Request failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries exceeded. Request failed.")
                raise


db=_mysql.connect("localhost","root","","crawler_db")

def keywords():
  for _ in range(3):
    try:
      db.query("CALL PROCEDURE_KEYWORDS_3_louisiana(@p,@p1);")
      db.query('SELECT @p AS `SR_NO`,@p1 AS `KEYWORD`') 
      r=db.store_result()
      results=r.fetch_row()
      SR_NO = results[0][0].decode()
      KEYWORD = results[0][1].decode()
    
      print('SR_NO :', SR_NO, 'KEYWORD :', KEYWORD)
      return KEYWORD
      
      
    except Exception as e: 
      print('Empty keyword / Deadlock issue', e)
      continue 




api_key = os.getenv('APIKEY_2CAPTCHA', 'your_2captcha_key')
solver = TwoCaptcha(api_key)
g_recaptcha_response = solver.recaptcha(sitekey="6LfX5QATAAAAAHneQ7BlFzpmJbfAk8nMTq29FlRC",
                          url='https://coraweb.sos.la.gov/CommercialSearch/CommercialSearch.aspx')


KEYWORD = keywords()
max_retries = 5
retry_delay = 3
session = requests.Session()
url = "https://coraweb.sos.la.gov/CommercialSearch/CommercialSearch.aspx"

payload_1 = {
    '__EVENTTARGET': 'ctl00$cphContent$btnSearch',
    '__EVENTARGUMENT': '',
    '__LASTFOCUS': '',
    '__VIEWSTATE': 'S2aVCbBr+ILSHysxd3Ok77faIo0FoStJ7yOPpYbbqGPahzzt6AV/7maR2xdcApNnQVE3vVTGGo29QAguuiqZPAG2OK2Rcn7o1JHuhd96xk9Gr/QrSNnRAFQDSxbikkhdphtR0Par/6HezR1tqgrznnv6mSiB3E7T/ppKJPvX0vOngVFp0b+rVoI5AUQSQP/VBY1iptjSsWbNfO0DkcPw2JdUJatBpbilBFUKbS48sEOc6mJKbUCxeG644FXHpkp++mDePkZUJd3IJB9J6H5cUzPqOGwyKwZxzgWMBg5hjb7ZX9ZtrPBYsbYPSOol0FkThd9SruAZ9yXEopSn2YkQIjz7uvnxZQ0t8IygJySZWmW4TS+Rio9KPDXipKODqfK41IjMgE6LJIHhvwy2jPOKAFNMTbH5lPRJm0gXPp2eQdn0s1YLbpQK/NQ6AjDcqum2lHape+swr/FURMJE+9HyKEHpaJwgySHzcFJd2fQm8aZTyLFJlilSQdMRsENuQKCpNv/eiucIGpTVDARbax3lKKqQ1mC2IkvXU3pbtbSXqCN0tCZ4YqeMGM39gKu1iNj2dafF+yNw1AXfC7MmCu8hyuwcYz94jM1rw7Cf0qMAWIHa14f8n3hGibn3RJdne2DeTdnGotlUAZECB7FQx3NBRCMpDnVPhKffXczX0GzVs05IHPQX3bp5gTitnhJECuHsO4OiR1KCK9mwEi1BzwCvjCaeZnYmQDFcubDqZK734xcD5GCBqGG+vWEnPxYGb2DbfMqrpfjX5YOiq81vJrLtFEoo/mXcfgqFrGqs3GFsYn5nEWdK92aoXxozuBywO5WiBhkGPX31M6Cf+eTzjSGYfS0LMRUcrk1LF8gNw/r6SK0YRn/vXu3AtPJKMlY/FpB1pEYDYkSKd++yHXQmO683B3EthbFel8H01oUIyyadXuvzhOy8u0AQX/yB9aJGApI1CyA3goQL0Xdnsibv/GJSca9EmNC2OHYq+q+GUoz7ETuuC2pQpS47RQ1jADgNGC4X+AsY3bkCnD0VnNryvU8t19TusIh9Rjc36u0Oz4Iy4VdkBqH+',
    '__VIEWSTATEGENERATOR': '639EFE92',
    '__EVENTVALIDATION': '5Fln+QDCkCwi5tREruxIViGeOdZ9J0w365t4UOJujRs7gx/AzmAj1dAzxkAg6xNk8nM67FLcJi8PJ7/3LQPR4ou2D8/4JqsotwdwWijkmuNAsKVkvLedeNl+hA58G/jYufwp1+i+YN15dP9D2CR9GjV8ShFqxyGWC+jeKFk7Yj4+bCs0aPh24HbxMQeLtPsYr8KMtK4KOgWjZ2so7oEWWxm5yHcnWruMWC9a6xxut+6qJqOpifV8RlGhSf9Va/oapFqOQhwPnKh6IGcYi7PvBTUbKTZrSnHAV1N7kEI3CruyWblF',
    'ctl00$hdnTimeoutsDisabled': 'false',
    'ctl00$cphContent$grpSearch': 'radSearchByEntity',
    'ctl00$cphContent$txtEntityName': f'{KEYWORD}',
    'ctl00$cphContent$txtCharterNumber': '',
    'ctl00$cphContent$txtFirstName': '',
    'ctl00$cphContent$txtLastName': '',
    'g-recaptcha-response': g_recaptcha_response['code']
}

headers = {
    'Referer': 'https://coraweb.sos.la.gov/CommercialSearch/CommercialSearch.aspx',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

try:
  response_1 = make_request_with_retry(url, headers, payload_1, max_retries, retry_delay)
  html_content = response_1.text

  if response_1.status_code == 200:
      soup = BeautifulSoup(html_content, 'html.parser')

      viewstate = soup.find('input', {'id': '__VIEWSTATE'})['value']
      viewstate_generator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
      event_validation = soup.find('input', {'id': '__EVENTVALIDATION'})['value']

      target_tr = soup.find('tr', class_='BlackBold')
      try:
        if target_tr:
          a_tags = target_tr.find_all('a')
          last_page = a_tags[-1].get_text()
          print("Last Page Number:", last_page)
        else:
          last_page = 1

      except (AttributeError, IndexError, ValueError) as e:
          print("Error extracting last page number:", e)
          last_page = 1

      # print('__VIEWSTATE:', viewstate)
      # print('__VIEWSTATEGENERATOR:', viewstate_generator)
      # print('__EVENTVALIDATION:', event_validation)
  
  else:
    print("Failed to fetch data from response_1. Status code:", response_1.status_code)

except Exception as e:
  print('An Error Occurred in response_1:',e)


for j in range(0,int(last_page)):
  y = str(j).zfill(2)
  payload_3 = {'__EVENTTARGET': f'ctl00$cphContent$grdSearchResults_EntityNameOrCharterNumber$ctl29$ctl{y}',
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': viewstate,
    '__VIEWSTATEGENERATOR':viewstate_generator,
    '__EVENTVALIDATION':event_validation,
    'ctl00$hdnTimeoutsDisabled': 'false',
    'ctl00$cphContent$hdnCurrentSearchType': 'EntityName'}
  
  time.sleep(random.uniform(1,6))
  try:
    response_3 = make_request_with_retry(url, headers, payload_3, max_retries, retry_delay)
    # print(display(HTML(response_3.text)))

    html_content_1 = response_3.text

    if response_3.status_code == 200:
        soup_1 = BeautifulSoup(html_content_1, 'html.parser')

        viewstate_1 = soup_1.find('input', {'id': '__VIEWSTATE'})['value']
        viewstate_generator_1 = soup_1.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
        event_validation_1 = soup_1.find('input', {'id': '__EVENTVALIDATION'})['value']

        row_normal = soup_1.find_all('tr', class_='RowNormal')
        row_alt = soup_1.find_all('tr', class_='RowAlt')
      
        if row_normal or row_alt:
          total_count = len(row_normal)+len(row_alt)+5             #add 5 number for extra hitting 
          print('total count:', total_count)
        else:
          print("data is not prasent on page")
          break

        # print('__VIEWSTATE:', viewstate_1)
        # print('__VIEWSTATEGENERATOR:', viewstate_generator_1)
        # print('__EVENTVALIDATION:', event_validation_1)
    else:
      print("Failed to fetch data. Status code:", response_3.status_code)

  except Exception as e:
    print('An Error Occurred in response_3',e)  
  
  for i in range(0,int(total_count)):
    hit_moniter_api('Louisiana.json')
    x = str(i).zfill(2)
    payload_2 = {'__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': viewstate_1,
    '__VIEWSTATEGENERATOR': viewstate_generator_1,
    '__EVENTVALIDATION': event_validation_1,
    'ctl00$hdnTimeoutsDisabled': 'false',
    'ctl00$cphContent$hdnCurrentSearchType': 'EntityName',
    f'ctl00$cphContent$grdSearchResults_EntityNameOrCharterNumber$ctl{x}$btnViewDetails': 'Details'}

    
    time.sleep(random.uniform(1,5))
    try:
      response_2 = make_request_with_retry(url, headers, payload_2, max_retries, retry_delay)
      html_data = response_2.text

      if 'records are shown in' not in html_data:
        soup_2 = BeautifulSoup(html_data, 'html.parser')
        charter_number_element = soup_2.find('span',id='ctl00_cphContent_lblCharterNumber')
        if charter_number_element:
          charter_number = charter_number_element.text.strip()

          with open(f"html/{charter_number}.html","w",encoding="utf-8") as file:
            file.write(html_data)
            print(f"{charter_number}.html download successfully")
        
        else:
          span_element = soup_2.find('span', id='ctl00_cphContent_lblServiceName')

          original_text = span_element.get_text()
          modified_text = ''.join(c if c.isalnum() else '_' for c in original_text)
          with open(f"HTML_FILE/{modified_text}.html","w",encoding="utf-8") as file:
            file.write(html_data)
            print("file download but charter number not found")

          try:
            subprocess.run(["aws", "s3", "mv", "./HTML_FILE/", "s3://dev_buk/DATA/XSUSREG/US-LA/invalid_HTML/", "--recursive", "--exclude", "*", "--include", "*.html"], check=True)
          except: pass
      
    except Exception as e:
      print("An Error Occurred in response_2",e)


try:
  subprocess.run(["aws", "s3", "mv", "./html/", "s3://dev_buk/DATA/XSUSREG/US-LA/HTML/", "--recursive", "--exclude", "*", "--include", "*.html"], check=True)
except: pass



