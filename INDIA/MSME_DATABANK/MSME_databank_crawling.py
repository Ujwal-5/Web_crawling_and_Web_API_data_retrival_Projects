import requests
from bs4 import BeautifulSoup 
import re
from PIL import Image
from io import BytesIO
from twocaptcha import TwoCaptcha
from IPython.display import HTML
import sys

session = requests.Session()
home_url = "https://www.msmedatabank.in/Info/Verify.aspx"
home_response = session.get(home_url)
# print(home_response.text)
# sys.exit()
soup = BeautifulSoup(home_response.text, 'html.parser')

event_state_input = soup.find('input', {'id': '__VIEWSTATE'})
event_state_value = event_state_input.get('value', '') if event_state_input else ''

event_validation_input = soup.find('input', {'id': '__EVENTVALIDATION'})
event_validation_value = event_validation_input.get('value', '') if event_validation_input else ''

event_viewgen_input = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})
event_viewgen_value = event_viewgen_input.get('value', '') if event_viewgen_input else ''

print("Event state value: ", event_state_value)
print("Event validation value: ", event_validation_value)
print("Event viewstate generator value:", event_viewgen_value)

middle_headers = {
  'Host': 'www.msmedatabank.in',
  'Origin': 'https://www.msmedatabank.in',
  'Referer': 'https://www.msmedatabank.in/Info/Verify.aspx',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

middle_payload = {
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    '__LASTFOCUS': '',
    '__VIEWSTATE': event_state_value,
    '__VIEWSTATEGENERATOR': event_viewgen_value,
    '__EVENTVALIDATION': event_validation_value,
    'ctl00$MainContent$ddRegType':'UDYAM',
    'ctl00$MainContent$txCaptcha':'',

}

middle_response = session.post(home_url, data = middle_payload, headers=middle_headers)
soup_middle = BeautifulSoup(middle_response.text, 'html.parser')

event_state_input_middle = soup_middle.find('input', {'id': '__VIEWSTATE'})
event_state_value_middle = event_state_input_middle.get('value', '') if event_state_input else ''

event_validation_input_middle = soup_middle.find('input', {'id': '__EVENTVALIDATION'})
event_validation_value_middle = event_validation_input_middle.get('value', '') if event_validation_input else ''

event_viewgen_input_middle = soup_middle.find('input', {'id': '__VIEWSTATEGENERATOR'})
event_viewgen_value_middle = event_viewgen_input_middle.get('value', '') if event_viewgen_input else ''

print("Event state value: ", event_state_value_middle)
print("Event validation value: ", event_validation_value_middle)
print("Event viewstate generator value:", event_viewgen_value_middle)

regex_pattern_middle = r'CaptchaImage\.axd\?guid=([a-fA-F0-9\-]{36})'

match_middle = re.search(regex_pattern_middle, middle_response.text)
if match_middle:
    guid = match_middle.group(1)  # Use group(1) to get only the GUID part
    print(f"GUID: {guid}")
else:
    print("No GUID found.")
    

captcha_response = session.get(f"https://www.msmedatabank.in/Info/CaptchaImage.axd?guid={guid}")

captcha_image = Image.open(BytesIO(captcha_response.content))
captcha_image.save('captcha.png')
# captcha_image.show()

solver = TwoCaptcha('your_2captcha_key')
result = solver.normal('captcha.png')
captcha_value = result['code']

print("Captcha value: ", captcha_value)

udyam_number = 'UDYAM-MH-26-0229699'

# result_payload = f'_EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE={event_state_value}&__VIEWSTATEGENERATOR={event_viewgen_value}&__EVENTVALIDATION={event_validation_value}&ctl00%24MainContent%24ddRegType=UDYAM&ctl00%24MainContent%24txUAM={udyam_number}&ctl00%24MainContent%24txCaptcha={captcha_value}'

result_payload = {
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    '__LASTFOCUS': '',
    '__VIEWSTATE': event_state_value_middle,
    '__VIEWSTATEGENERATOR': event_viewgen_value_middle,
    '__EVENTVALIDATION': event_validation_value_middle,
    'ctl00$MainContent$ddRegType':'UDYAM',
    'ctl00$MainContent$txUAM':udyam_number,
    'ctl00$MainContent$txCaptcha':captcha_value.upper(),
    'ctl00$MainContent$btnVerify': 'Verify Details'

}
print(result_payload)

result_headers = {
  'Host': 'www.msmedatabank.in',
  'Origin': 'https://www.msmedatabank.in',
  'Referer': 'https://www.msmedatabank.in/Info/Verify.aspx',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

result_response = session.post(home_url, headers = result_headers, data = result_payload)
# print(display(HTML(result_response.text)))

with open('result.html', 'w', encoding='utf-8') as f:
    f.write(result_response.text)

