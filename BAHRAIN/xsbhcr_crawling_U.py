import json
import boto3
from botocore.exceptions import ClientError
import traceback
import mysql.connector
from mysql.connector import Error
import os
import botocore
import cloudscraper
import time
import random
import requests
import subprocess


print("Script started")
conf = open('json/bhcr.json') 
conFile = json.load(conf)   
branch_no = conFile['Branch']
class DbService:
    connection = None
    connection_mappings = None

    def __init__(self):         
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                passwd='',
                database='crawler_db',
                port='3306'
            )

            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    def close(self):
        # self.connection_mappings.close()
        self.connection.close()

    def get_a_record(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("CALL PROCEDURE_URL_BHCR(@p0, @p1)")
            # Fetch the output parameters
            cursor.execute("SELECT @p0 AS `SL_NO`, @p1 AS 'CR_NO'")
            output_params = cursor.fetchone()
            KEYWORD = output_params[1]
            print('KEYWORD:', KEYWORD)
            cursor.close()
            return KEYWORD
        except mysql.connector.Error as e:
            print(f"An error occurred while executing the database query: {e}")
            cursor.close()
            return database_service.get_a_record(self)
        
    def get_aut_key(self, max_retries=3, retry_delay=1):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT AUTH_KEY FROM URL_BHCR_AUTHORIZATION_KEY WHERE STATUS = 0")
            results = cursor.fetchall()
            # Update the status to 9 for the selected rows
            if results:
                aut_key = results[0][0]
                print('aut_key', aut_key)
                self.connection.commit()
                print(f"Authentication key used")
                return str(aut_key)
        except mysql.connector.Error as e:
            print(f"An error occurred while executing the database query: {e}")
            cursor.close()
            if max_retries > 0:
                print("Retrying in a moment...")
                time.sleep(retry_delay)
                return self.get_aut_key(max_retries=max_retries-1, retry_delay=retry_delay)
            else:
                print("Maximum retries reached. Returning None.")
                return None

    def exp_aut_key(self, authentification_key, max_retries=3, retry_delay=1):
        cursor = self.connection.cursor()
        try:
            update_exp = f"UPDATE `URL_BHCR_AUTHORIZATION_KEY` SET `STATUS` = 1 WHERE `AUTH_KEY` = '{authentification_key}'"
            print(update_exp)
            cursor.execute(update_exp)
            # Commit the changes
            self.connection.commit()
            print(f"Authentication set expiration")

        except mysql.connector.Error as e:
            print(f"An error occurred while executing the database query: {e}")
            cursor.close()
            if max_retries > 0:
                print("Retrying in a moment...")
                time.sleep(retry_delay)
                return self.exp_aut_key(authentification_key, max_retries=max_retries-1, retry_delay=retry_delay)
            else:
                print("Maximum retries reached. Returning None.")
                return None

    def update_the_record_10(self, KEYWORD):
        cursor = self.connection.cursor()
        query = f"UPDATE TEMP_URL_BHCR_{branch_no} SET BRANCH_{branch_no} = 10 WHERE `CR_NO` = '{KEYWORD}'"
        print(query)
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return False

    def update_the_record_5(self, KEYWORD):
        cursor = self.connection.cursor()
        query = f"UPDATE TEMP_URL_BHCR_{branch_no} SET BRANCH_{branch_no} = 5 WHERE `CR_NO` = '{KEYWORD}'"
        print(query)
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return False


database_service = DbService()        
# Example usage
authentification_key = database_service.get_aut_key()      
loop = 0
while True:
    for _ in range(10):
        try:
            try:
                requests.get('http://3.254.232.204/DEV2.0/Configrator/monitor.php?Browser='+conFile['Browser']+'&Service='+conFile['Service']+'&Machine_Name='+conFile['Machine_Name'])    
            except: pass
            data = database_service.get_a_record()
            url = "https://api.sijilat.bh/api/CRdetails/CompleteCRDetails"

            payload = json.dumps({
                "cr_no": str(data),
                "branch_no": branch_no,
                "cult_lang": "EN",
                "Input_CULT_LANG": "EN",
                "cultLang": "EN",
                "CurrentMenuTyp": "A",
                "CurrentMenu_Type": "A",
                "cpr_no": "",
                "CPR_NO_LOGIN": "",
                "CPR_GCC_NO": "",
                "CPR_OR_GCC_NO": "",
                "Login_CPR_No": "",
                "Login_CPR": "",
                "cprno": "",
                "LOGIN_PB_NO": "",
                "PB_NO": "",
                "SESSION_ID": "n45aw3zr2chr3sedhnsfhc4p"
            })
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': authentification_key,
                'Cookie': 'AWSALB=5pni1jrhCadCbqJlLcrIaf+bBjpovxfZDYdGTFH9EBEu2g5L0zrHzivXMRk/MOcRjPYht3YoyQEKV+5Vo7c5VAdOyodnhLPs+y1djNyI8m2w/Q3ImPT1L56PKI; AWSALBCORS=5pni1jrhCadCbqJlLcrIaf+bBjpovxfZDYdGTFH9EBEu2g5L0zrHzivXMRk/MOcRjPYht3YoyQEKV+5Vo7c5VAdOyodnhLPs+y1djNyI8m2w/Q3ImPT1L56PKI'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            data_dict = response.json()
            print(data_dict)
            if "jsonData" in data_dict and data_dict["jsonData"] is not None and "company_summary" in data_dict["jsonData"]:
                print(1)
                cr_no = data_dict["jsonData"]["company_summary"].get("CR_NO")
                if cr_no is not None:
                    with open(f'{data}-2.json', "w", encoding="utf-8") as json_file:
                        json.dump(response.json(), json_file, ensure_ascii=False)
                    # json_file = f'{data}.json'
                    print("successful saved", f'{data}-{branch_no}.json')
                    database_service.update_the_record_10(data)
                else:
                    print("Exception.",data)
                    database_service.update_the_record_5(data)


            elif "Message" in data_dict and data_dict['Message']== "No Data Found.":
                print("No Data Found.",data)
                database_service.update_the_record_5(data)

            elif 'Message' in data_dict and data_dict['Message'] == 'Authorization has been denied for this request.':
                print(3)
                print('retrying to get new Authorization key')
                database_service.exp_aut_key(authentification_key)
                time.sleep(2*60)
                authentification_key = database_service.get_aut_key()
                pass

            else: 
                print(4)
                print("New type of file")

        except Exception as e:
            print('Error:', e)
            traceback.print_exc()

        # finally:
            #db.close()
            # s.close()
    try:
        subprocess.run(["aws", "s3", "mv", "./", f"s3://dev_buk/DATA/BHCR/BRANCH_{branch_no}/", "--recursive", "--exclude", "*", "--include", "*.json"], check=True)
    except: pass
