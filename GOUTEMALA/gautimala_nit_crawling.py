from bs4 import BeautifulSoup
import re
import requests
from twocaptcha import TwoCaptcha
import base64
import os
from PIL import Image
from io import BytesIO
from urllib.parse import quote
import time
import sys
from lxml import html
import string
import csv
import concurrent.futures

# Function to write a set to a CSV file
def write_set_to_csv(data_set, csv_filename):
    # Open the CSV file in write mode
    with open(csv_filename, 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Iterate over the set and write each element as a new row
        for item in data_set:
            writer.writerow([item])

csv_filename = 'nit_list.csv'

# "." = "A"
gua_type = ['1', '2', '3', '4', '6', '7', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '61', '-1']
# for "." in string.ascii_uppercase:
    # Loop through gua_type values
def collect_nit_numbers(gua):
    nit_list = set()
    nit_test = []
    session = requests.Session()
    url = "https://www.guatecompras.gt/proveedores/busquedaProvee.aspx"
    home_response  = session.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(home_response.text, 'html.parser')

    # Find the image tag
    img_tag = soup.find('img', id='MasterGC_ContentBlockHolder_CaptchaValidacion_CaptchaImage')

    # Extract the src attribute
    src = img_tag['src'] if img_tag else ''

    # Use regex to extract the GUID from the src
    match = re.search(r'guid=([a-f0-9\-]+)', src)

    # Check if a match is found and print the GUID
    if match:
        guid = match.group(1)
    #     print(f"Extracted GUID: {guid}")
    # else:
    #     print("GUID not found in the src attribute.")

    captcha_headers = {
      'authority': 'www.guatecompras.gt',
    #   'cookie': '_ga=GA1.1.220698957.1724669004; TKGC=jLvRCQ2t1bUyalVf6JDy9Ja5QzmlmGRD; SSGC=nxrjiymdx42o22refx4pp1hj; MINFIN-per=!oQutmMzAWim6w/T5Y26Gud5prDLya/zVQ0GDOa0x49dQtihs8cwSW6CoW50tHQOIoYLPw/rMNZtWJFA=; __cf_bm=2XzTrpN6D1hgot8AWPUNfPhqWtBFa7je7RVhIcX6wns-1725348576-1.0.1.1-bcXYbZWjXR6k5emYFudgTxKJN.4RtSIXELVRNDrYmPcapKQo67UOu9CLTlURCPCnMwMJ686llnWpQzE6J7jSmg; TS01f1674b=015b894ff6ed3a92e3c623405ae32babeab155f2fd687d42d802a0cf4c0edd1633ba3cc86ba55e9b02a57691b9b3fc10ad46ebe52b7c8b188bf049fed1ba37ca82a1cbc6d5d23deb089b7b3a610a7adb9ad64005c1; _ga_25H8H8TS93=GS1.1.1725348578.6.1.1725349427.0.0.0; cf_clearance=96_JcOC6FAz3NB9xmWRVHCKTTiMk76AaWmgeQHBZl1A-1725349431-1.2.1.1-G407LtScWfp6swrLmK5hffwpyHGzB1gwLXh6rz9pJ.6R4ZIKf3CpbDu_Ym2MNgQLWfZH1M6_W_BEIPT89xErZgz8mf1gO5YOkN1XY8P2bcHTnfkLudbNzQe7KpE2chDJgdT93WxZr_L4qfwKpc7USy1k42WvbUPr6pkz9wg0uCfu1xkgHDW4ltMr_PWRe45tl6csGg24d1wtmfzDbWO1coND6zI6lwelH1WrqfXARAiBjJUaR9866iZWT5Tr0lU_EIoAxdDVRPP2l_trChMXGNg3JcW0fEENI57oqJCmkUus4kjd4cdKrR2c3z_610uj7Y5uftLcejO3ekvX6PcoINEE_l2RBs4J9wg7G142sVgAKZvnJ2Ipluoo9iMJbpoi; __cf_bm=yvZWfDYCZJYBwjm52HMFkggFixFvdQ85hJv_ZfqFz0M-1725351158-1.0.1.1-NpX8pZ4yN_.zOG6uKauIGxC.1OpDq.lz1tIuDAHeLRESt77jl32IOryMQOQ6swohlxv26g23Bqke1zqcGIEssg; MINFIN-per=!NwqDkvFhMpcA+2j5Y26Gud5prDLya6qI5EXz9Z4uC5KFkzDiCl3SqmsuHk2ImbjPMLHB0S2ZhfNP3j0=; SSGC=a0mvklg3tiskefetuj0t135s; TS01f1674b=015b894ff6bb7a67fe5b6e7d0e974ad5bea67113780fbb172f55d5d5d9440ea127d982a24d72d6639365bd4bcafda0bd9493f24136e8bd2d0e7924f3bb4270161b402803795421c3a41a4457e5aa2d3b56b0325c42',
      'referer': 'https://www.guatecompras.gt/proveedores/busquedaProvee.aspx',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }
    captcha_response = session.get(f"https://www.guatecompras.gt/Telerik.Web.UI.WebResource.axd?type=rca&isc=true&guid={guid}", headers=captcha_headers)

    base64_image = base64.b64encode(captcha_response.content).decode('utf-8')

    api_key = os.getenv('APIKEY_2CAPTCHA', 'your_2captcha_key')
    solver = TwoCaptcha(api_key)
    result = solver.normal(base64_image)
    # print(result)

    captcha_value = result['code']
    # Fetch the value of __VIEWSTATE
    viewstate_element = soup.find('input', {'id': '__VIEWSTATE'})
    viewstate = viewstate_element['value'] if viewstate_element else ""

    # Fetch the value of __VIEWSTATEGENERATOR
    viewstate_generator_element = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})
    viewstate_generator = viewstate_generator_element['value'] if viewstate_generator_element else ""

    # Fetch the value of __EVENTVALIDATION
    eventvalidation_element = soup.find('input', {'id': '__EVENTVALIDATION'})
    eventvalidation = eventvalidation_element['value'] if eventvalidation_element else ""

    # Fetch the value of __EVENTTARGET
    eventtarget_element = soup.find('input', {'id': '__EVENTTARGET'})
    eventtarget = eventtarget_element['value'] if eventtarget_element else ""

    # Print values for debugging
    # print(f"VIEWSTATE: {viewstate}")
    # print(f"VIEWSTATEGENERATOR: {viewstate_generator}")
    # print(f"EVENTVALIDATION: {eventvalidation}")
    # print(f"EVENTTARGET: {eventtarget}")
    # print(viewstate_encoded)
    # print(viewstate_generator)

    final_payload = {
        "MasterGC$ContentBlockHolder$scriptManager": "MasterGC$ContentBlockHolder$upnFiltros|MasterGC$ContentBlockHolder$ctl04$ddlBusCarEn",
        "MasterGC$ContentBlockHolder$txtNit": "",
        "MasterGC$ContentBlockHolder$TextBox7": "",
        "MasterGC$ContentBlockHolder$txtCUI": "",
        "MasterGC$ContentBlockHolder$txtNuevaBusquedaNombre": ".",
        "MasterGC$ContentBlockHolder$TextBox5": "",
        "MasterGC$ContentBlockHolder$Accordion1_AccordionExtender_ClientState": "0",
        "MasterGC$ContentBlockHolder$ctl04$ddlBusCarEn": gua,
        "MasterGC$ContentBlockHolder$ctl04$ddlOpcionesNombre": "2",
        "MasterGC$ContentBlockHolder$ctl04$ddlTipo": "3",
        "MasterGC$ContentBlockHolder$CaptchaValidacion$CaptchaTextBox": captcha_value,
        "MasterGC_ContentBlockHolder_CaptchaValidacion_ClientState": "",
        "__EVENTTARGET": "MasterGC$ContentBlockHolder$ctl04$ddlBusCarEn",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__VIEWSTATE": viewstate,
        "__VIEWSTATEGENERATOR": viewstate_generator,
        "__EVENTVALIDATION": eventvalidation,
        "__ASYNCPOST": "true",
        "MasterGC$ContentBlockHolder$ValidarCaptcha": "Validar"
    }
      

    final_headers = {
      'authority': 'www.guatecompras.gt',
      'accept-language': 'en-US,en;q=0.9',
      'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'origin': 'https://www.guatecompras.gt',
      'referer': 'https://www.guatecompras.gt/proveedores/busquedaProvee.aspx',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
      'x-microsoftajax': 'Delta=true',
      'x-requested-with': 'XMLHttpRequest',
      # 'Cookie': 'MINFIN-per=!PjkEOn8JTiROLgH5Y26Gud5prDLyazl10vyw/BOUjpq9tnHrTjEtKIowg8OUUiNMZdt7HORJtW4X6vQ=; SSGC=52uuyxemce5brthjapeh4fbi; TS01f1674b=015b894ff66a005f888b4bdcb0eed175109cf0d026ea5f7a6b7425338d6ee13a8fc1690b81c8eaf3bf3a9dfaa39a476831b17cf2f39b64a4a55db693317cf50dc189133e609f3fa9f7e6d8faf728272d0faf836dce'
    }

    final_response = session.post(url, data=final_payload, headers=final_headers)
    pattern = r'<\/td><td>&nbsp;<\/td><td>(.*?)<\/td>'

    # Find all matches in the text
    matches = re.findall(pattern, final_response.text)

    # Print the list of matched values
    # print(matches)
    nit_list.update(matches)
    nit_test+=matches
    # print(matches)
    if matches !=[]:
      # print("Captcha failed retrying")
      collect_nit_numbers(gua)

    # Parse the HTML
    soup = BeautifulSoup(final_response.text, 'html.parser')
    # Split the content based on the unique `|__VIEWSTATE|`
    html_final = final_response.text
    view_parts = html_final.split('|__VIEWSTATE|')
    viewstate = view_parts[1].split('|')[0]
    view_gen_parts = html_final.split('|__VIEWSTATEGENERATOR|')
    viewstate_generator = view_gen_parts[1].split('|')[0]
    ev_parts = html_final.split('|__EVENTVALIDATION|')
    eventvalidation = ev_parts[1].split('|')[0]

    span = soup.find('span', id='MasterGC_ContentBlockHolder_lblFilas2')
    # print(span)
    if span:
        # Extract the text
        text = span.get_text()

        # Use regex to find the number
        match = re.search(r'de ([\d,]+) proveedores', text)
        if match:
            total_providers = match.group(1)
            print(total_providers)  # Output: 1,039
            for i in range(2, int(int(total_providers.replace(',','')) / 25)+3):
              print("total loop numbesrs are", int(int(total_providers.replace(',','')) / 25))
              print('current loop number is', i)
              individual_payload = {
                    'MasterGC$ContentBlockHolder$scriptManager': 'MasterGC$ContentBlockHolder$upnResultado|MasterGC$ContentBlockHolder$gvResultado',
                    'MasterGC$ContentBlockHolder$txtNit': '',
                    'MasterGC$ContentBlockHolder$TextBox7': '',
                    'MasterGC$ContentBlockHolder$txtCUI': '',
                    'MasterGC$ContentBlockHolder$txtNuevaBusquedaNombre': ".",
                    'MasterGC$ContentBlockHolder$TextBox5': '',
                    'MasterGC$ContentBlockHolder$Accordion1_AccordionExtender_ClientState': '0',
                    'MasterGC$ContentBlockHolder$ctl04$ddlBusCarEn': gua,
                    'MasterGC$ContentBlockHolder$ctl04$ddlOpcionesNombre': '2',
                    'MasterGC$ContentBlockHolder$ctl04$ddlTipo': '3',
                    'MasterGC$ContentBlockHolder$CaptchaValidacion$CaptchaTextBox': '',
                    'MasterGC_ContentBlockHolder_CaptchaValidacion_ClientState': '',
                    '__EVENTTARGET': 'MasterGC$ContentBlockHolder$gvResultado',
                    '__EVENTARGUMENT': f'Page${i}',
                    '__LASTFOCUS': '',
                    '__VIEWSTATE': viewstate,
                    '__VIEWSTATEGENERATOR': viewstate_generator,
                    '__EVENTVALIDATION': eventvalidation,
                    '__ASYNCPOST': 'true'
                }
                            

              individual_headers = {
                'authority': 'www.guatecompras.gt',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://www.guatecompras.gt',
                'referer': 'https://www.guatecompras.gt/proveedores/busquedaProvee.aspx',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
                'x-microsoftajax': 'Delta=true',
                'x-requested-with': 'XMLHttpRequest',
                # 'Cookie': 'MINFIN-per=!PjkEOn8JTiROLgH5Y26Gud5prDLyazl10vyw/BOUjpq9tnHrTjEtKIowg8OUUiNMZdt7HORJtW4X6vQ=; SSGC=52uuyxemce5brthjapeh4fbi; TS01f1674b=015b894ff66a005f888b4bdcb0eed175109cf0d026ea5f7a6b7425338d6ee13a8fc1690b81c8eaf3bf3a9dfaa39a476831b17cf2f39b64a4a55db693317cf50dc189133e609f3fa9f7e6d8faf728272d0faf836dce'
              }

              individual_response = session.post(url, data=individual_payload, headers=individual_headers)
              # print(individual_response.text)
              pattern = r'<\/td><td>&nbsp;<\/td><td>(.*?)<\/td>'

              # Find all matches in the text
              matches = re.findall(pattern, individual_response.text)

              # Print the list of matched values
              # print(matches)
              nit_list.update(matches)
              nit_test+=matches
              # print(matches)
              # print('list', len(nit_test))
              # print(len(nit_list))
              if matches !=[]:
                view_parts = individual_response.text.split('|__VIEWSTATE|')
                viewstate = view_parts[1].split('|')[0]
                view_gen_parts = individual_response.text.split('|__VIEWSTATEGENERATOR|')
                viewstate_generator = view_gen_parts[1].split('|')[0]
                ev_parts = individual_response.text.split('|__EVENTVALIDATION|')
                eventvalidation = ev_parts[1].split('|')[0]
              # time.sleep(3)
              # sys.exit()
        else:
          print("No match found for total providers.")
      
          
    # print(nit_list)
    # print(len(nit_list))
    write_set_to_csv(nit_list, csv_filename)


with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    # Map the crawlData method to each keyword
    futures = {executor.submit(collect_nit_numbers, gua): gua for gua in gua_type}
    results = {}
    for future in concurrent.futures.as_completed(futures):
        keyword = futures[future]
        try:
            result, status = future.result()
            results[keyword] = (result, status)
        except Exception as exc:
            results[keyword] = (None, str(exc))

        # sys.exit()