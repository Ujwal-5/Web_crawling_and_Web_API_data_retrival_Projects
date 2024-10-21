import mysql.connector
from mysql.connector import Error
from settings import MYSQL
import time

class DbService:
    connection = None
    connection_mappings = None
    max_retries = 3
    retry_delay = 5  # seconds

    def __init__(self):
        self.connect()

    def connect(self):
        attempt = 1
        while attempt <= self.max_retries:
            try:
                self.connection = mysql.connector.connect(
                    host=MYSQL['url'],
                    user=MYSQL['username'],
                    passwd=MYSQL['password'],
                    database=MYSQL['schema'],
                    port=MYSQL['port']
                )
                print("Connection to MySQL DB successful")
                return  # Connection successful, exit loop
            except Error as e:
                print(f"Attempt {attempt}: The error '{e}' occurred while connecting to the database.")
                attempt += 1
                time.sleep(self.retry_delay)
        print("Max retry attempts reached. Unable to connect to the database.")

    def close(self):
        if self.connection:
            self.connection.close()

    def update_the_cookie(self, session, createdat):
        cursor = self.connection.cursor()
        query = f"UPDATE DATA_XSHKAR_ICRIS_COOKIES SET COOKIE = '{session}', STATUS = 'READY FOR ADDTOCART', CREATE_DATE = '{createdat}' WHERE USER = 'HKOFFICE6'"
        print(query)
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return False
    
    def get_session(self, session, createdat):
        cursor = self.connection.cursor()
        query = f"SELECT COOKIE DATA_XSHKAR_ICRIS_COOKIES"
        print(query)
        cursor.execute(query)
        output_params = cursor.fetchone()
        session = output_params[0]
        self.connection.commit()
        cursor.close()
        return session

    def update_the_status(self, order_number):
        cursor = self.connection.cursor()
        query = f"UPDATE DATA_XSHKAR_ICRIS_COOKIES SET STATUS = 'READY FOR ADDTOCART', ORDER_ID = '{order_number}' WHERE USER = 'HKOFFICE6'"
        print(query)
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return False

    def validate_purchase(self):
        cursor = self.connection.cursor()
        brn = ''
        theid = ''
        query = f"SELECT ID, BRN, STATUS FROM DATA_XSHKAR_ICRIS_COOKIES WHERE USER = 'HKOFFICE6'"
        print(query)
        cursor.execute(query)
        output_params = cursor.fetchone()
        theid = output_params[0]
        brn = output_params[1]
        value = output_params[2]
        print(value)
        if value == 'READY FOR PURCHASE':
            state = True
        elif value == 'READY FOR ADDTOCART':
            state = False
        else:
            state = False
        self.connection.commit()
        cursor.close()
        return state, theid, brn
