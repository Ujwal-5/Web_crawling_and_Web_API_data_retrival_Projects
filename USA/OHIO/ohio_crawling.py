import cloudscraper 
import json
from time import sleep
import random
import sys
from MySQLdb import _mysql


# fileName='AAA'
db=_mysql.connect("localhost","root","","crawler_db")

for _ in range(5):
    try:
        db.query("CALL PROCEDURE_KEYWORDS_3_ohio(@p);")
        db.query('SELECT @p AS `KEYWORD`') 
        r=db.store_result()
        results=r.fetch_row()
        fileName = results[0][0].decode()
        print('fileName :', fileName)
        break
    except Exception as e: 
        print('Empty fileName / Deadlock issue', e)
        # print(traceback.print_exc())
        continue  
else:
    sys.exit()

scraper = cloudscraper.create_scraper() 
#https://businesssearch.ohiosos.gov?=businessDetails/1670175
# Define the URL and headers
url = 'https://businesssearchapi.ohiosos.gov/NS_'+fileName+'_X?_=1715153403602'
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cookie': '__cf_bm=cBNYqVPSrsls0gjj8e9lp0A8O9HVyT6zqM55y4TSwDU-1715153278-1.0.1.1-xh0nJYW2MwwwQqhtuoJxXrXt_RHZKnPRK4GBfHdNbx22UJB.lqCOwJK.4TAem9QHkpa7Q7m1asN6oFXFheGLUQ; cf_clearance=UVKCDKvGgFfyE_8PAZSYUbrJpc0KZ2hmdRPI_m3fNZE-1715153279-1.0.1.1-ODVqU.Egfd4hYYcV1S3yzT5jt3Kb_WcRDUkWFdCyn9Ge_wXQAAKLaJeiSVbtKZfQ_tpUFQCztXvKw.rHGelU8Q',
    'origin': 'https://businesssearch.ohiosos.gov',
    'referer': 'https://businesssearch.ohiosos.gov/',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# Make the request
response = scraper.get(url, headers=headers)

# Print the response content
print(response.text)
with open('json/'+str(fileName)+'.json', 'w') as f:
        f.write(response.text)

data1 = json.loads(response.text)

# Extract and print charter_num for each business
for business in data1['data']:
    print("Charter Number:", business['charter_num'])
    companyUrl="https://businesssearchapi.ohiosos.gov/VD_"+business['charter_num']+"?_=1713777646789"
    print(companyUrl)
    companyResponce = scraper.get(companyUrl, headers=headers)
    print(companyResponce.text)
    with open('company_json/'+str(business['charter_num'])+'.json', 'w') as f:
        f.write(companyResponce.text)
        sleeptime = random.uniform(1, 10)
        print("sleeping for:", sleeptime, "seconds")
        sleep(sleeptime)
    


        
        