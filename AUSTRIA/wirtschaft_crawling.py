import requests
import json
import random
from MySQLdb import _mysql
import time
import subprocess
import traceback


db = _mysql.connect("localhost","root", "", "crawler_db")      
for _ in range(50):
    try:
        flag = True
        print('before flag')
        for _ in range(10):
            try:
                db.query('CALL `PROCEDURE_URL_WIRTSCHAFT`(@p0, @p1); ')
                db.query("SELECT @p0 AS `id`, @p1 AS `keyword`;")
                break
            except Exception as e: 
                print(e)
                continue

        r=db.store_result()
        results=r.fetch_row()
        keyword = results[0][1].decode()
        print(keyword)

        time.sleep(random.uniform(1,3))
        url = f'https://www.wirtschaft.at/_next/data/2024.016.2/de/u/{keyword}.json?id={keyword}'
        response = requests.get(url)
        if response.status_code ==200:
            with open(f"{keyword}.json", 'w', encoding='utf-8') as json_file:
                json.dump(response.json(), json_file, indent=4)
            print(f"{keyword}.json is saved")
            for _ in range(5):
                try:
                    query = f"UPDATE TEMP_URL_WIRTSCHAFT SET status = 10  WHERE company_id = '{keyword}'"
                    db.query(query)
                    break
                except:
                    continue
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

    subprocess.run(["aws", "s3", "mv", "./", "s3://dev_buk/DATA/SOURCE/WIRTSCHAFT/JSON/", "--recursive", "--exclude", "*", "--include", "*.json"], check=True)
except: pass

