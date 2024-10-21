import json
# import boto3
# from botocore.exceptions import ClientError
import traceback
import mysql.connector
from mysql.connector import Error
import os
# import botocore
import cloudscraper
import time
import random
import requests
import subprocess

print("Script started")
conf = open('xscansreg.json') 
conFile = json.load(conf)   

def validate_combined_data(combined_data):
    # Check if 'data' key exists
    if 'data' not in combined_data:
        return False, "'data' key is missing"

    data = combined_data['data']

    # Check if 'entityRegNumber' is set and not empty
    if 'entityRegNumber' not in data or not data['entityRegNumber']:
        return False, "'entityRegNumber' is missing or empty"

    # Check if 'entityTypeDesc' is not "Related Party"
    if 'entityTypeDesc' in data and data['entityTypeDesc'] == "Related Party":
        return False, "'entityTypeDesc' cannot be 'Related Party'"

    # Check if 'personInd' is not true
    if 'personInd' in data and data['personInd']:
        return False, "'personInd' cannot be true"

    return True, "Validation successful"

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
            cursor.execute("CALL PROCEDURE_URL_XSCANSREG(@p0)")

            # Fetch the output parameters
            cursor.execute("SELECT @p0 AS `CR_NO`")
            output_params = cursor.fetchone()
            keyword = output_params[0]
            modified_string = keyword.replace("-", "")
            print('KEYWORD:', modified_string)
            cursor.close()
            return modified_string
        except mysql.connector.Error as e:
            print(f"An error occurred while executing the database query: {e}")
            cursor.close()
            return database_service.get_a_record(self)

    def update_the_record_10(self, KEYWORD):
        cursor = self.connection.cursor()
        query = "UPDATE TEMP_URL_XSCANSREG SET STATUS = 10 WHERE `CR_NO` = '%s'"%(KEYWORD)
        print(query)
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return False
    
    def update_the_record_5(self, KEYWORD):
        cursor = self.connection.cursor()
        query = "UPDATE TEMP_URL_XSCANSREG SET STATUS = 5 WHERE `CR_NO` = '%s'"%(KEYWORD)
        print(query)
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return False
    
    def update_the_record_2(self, KEYWORD):
        cursor = self.connection.cursor()
        query = "UPDATE TEMP_URL_XSCANSREG SET STATUS = 2 WHERE `CR_NO` = '%s'"%(KEYWORD)
        print(query)
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return False

    def insert_the_record(self, KEYWORD):
        cursor = self.connection.cursor()
        query = "INSERT INTO URL_XSCANSREG_NEW_2 (CR_NO) VALUES ('%s')"%(KEYWORD)
        print(query)
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return False
    
    def check_the_record(self, KEYWORD):
        cursor = self.connection.cursor()
        query = "SELECT CR_NO FROM URL_XSCANSREG_NEW_2 WHERE CR_NO = '%s'" % (KEYWORD)
        cursor.execute(query)
        output_params = cursor.fetchone()
        
        if output_params is not None:  # Check if a row was fetched
            keyword = output_params[0]
            cr_no = keyword
            print('KEYWORD:', cr_no)
            cursor.close()
            return cr_no
        else:
            print("No record found for KEYWORD:", KEYWORD)
            cursor.close()
        return 0




database_service = DbService()        
       
loop = 0
for _ in range(5):
    try:
        try:
            requests.get('http://3.254.232.204/DEV2.0/Configrator/monitor.php?Browser='+conFile['Browser']+'&Service='+conFile['Service']+'&Machine_Name='+conFile['Machine_Name'])    
        except: pass
        time.sleep(random.uniform(1, 3))
        scraper = cloudscraper.CloudScraper()
        modified_string = database_service.get_a_record()

        url =  f'https://api.rjsc.novascotia.ca/api/rjscentity/{modified_string}'
        url1 =  f'https://api.rjsc.novascotia.ca/api/rjscentity/allrelationships/{modified_string}'
        url2 = f'https://api.rjsc.novascotia.ca/api/rjscentity/latest-events/{modified_string}?maxNumEvents=5'
        url3 =  f'https://api.rjsc.novascotia.ca/api/entity/otheraddresses/{modified_string}'
        url4 =  f'https://api.rjsc.novascotia.ca/api/entity/names/{modified_string}'

        try:
            CR = database_service.check_the_record(KEYWORD=modified_string)
            # Check if there are any matching rows
            print('CR: ', CR, 'keyword :', modified_string)
            if int(CR)==int(modified_string):
                print(f"Number {modified_string} exists in the table.")
                continue

            else:
                response = scraper.get(
                    url=url,
                    timeout=20,
                )

                response1 = scraper.get(
                    url=url1,
                    timeout=20,
                )

                response2 = scraper.get(
                    url=url2,
                    timeout=20,
                )

                response3 = scraper.get(
                    url=url3,
                    timeout=20,
                )

                response4 = scraper.get(
                    url=url4,
                    timeout=20,
                )
                final_response = {}

                combined_data = {
                    'Profile': response.json(),
                    'Relationships': response1.json(),
                    'Events': response2.json(),
                    'Otheraddresses': response3.json(),
                    'Names': response4.json()                
                }

                # Print or use the final JSON response
                print("combined_data", combined_data)
                print(f"Number {modified_string} does not exist in the table.")
                if response.status_code == 200:
                    for relationship in combined_data["Relationships"]["data"]:
                        if validate_combined_data(combined_data) :
                            database_service.insert_the_record(KEYWORD=modified_string)
                            print("got required json")
                            database_service.update_the_record_10(modified_string)
                            print('updated database')
                            file_name = f'{modified_string}.json'
                            with open(file_name, "w", encoding="utf-8") as json_file:
                                json.dump(combined_data, json_file, ensure_ascii=False)
                                print("JSON data saved:", file_name)
                            break
                        else:
                            print("Invalid json")
                            database_service.update_the_record_5(modified_string)
                            pass

        except Exception as e:
            print('Error:', e)
            database_service.update_the_record_2(modified_string)
            traceback.print_exc()

    except Exception as e:
        print('Error:', e)
        traceback.print_exc()


try:
    subprocess.run(["aws", "s3", "mv", "./", f"s3://prod_buk/DATA/XSCANSREG/TODO/", "--recursive", "--exclude", "*", "--include", "*.json", "--exclude", "xscansreg.json"],check=True)
except: pass


