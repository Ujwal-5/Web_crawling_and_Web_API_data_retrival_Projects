import mysql.connector
from mysql.connector import Error
from settings import MYSQL

class DbService:
    connection = None
    connection_mappings = None   

    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host = MYSQL['url'],
                user = MYSQL['username'],
                passwd = MYSQL['password'],
                database = MYSQL['schema'],
                port = MYSQL['port']
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occured")

    def close(self):
        self.connection.close()
    
    def get_a_record(self, procedure_name, parameter):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"CALL {procedure_name}({parameter})")
            cursor.execute(f"SELECT {parameter}")
            output_params = cursor.fetchone()
            keyword = output_params[1]
            print('keyword :', keyword)
            cursor.close()
            return keyword
        except mysql.connector.Error as e:
            print(f"An error occured while executing the database query: {e}")
            cursor.close()
            DbService().get_a_record(self, procedure_name, parameter)


    def get_filingGuid_record(self, procedure_name, parameter):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"CALL {procedure_name}({parameter})")
            cursor.execute(f"SELECT {parameter}")
            output_params = cursor.fetchone()
            filingGuid = output_params[1]
            print('filingGuid :', filingGuid)
            cursor.close()
            return filingGuid
        except mysql.connector.Error as e:
            print(f"An error occured while executing the database query: {e}")
            cursor.close()
            DbService().get_filingGuid_record(self, procedure_name, parameter)
        
    def update_the_record(self, status, table, column, status_column, keyword):
        cursor = self.connection.cursor()
        query = f"UPDATE {table} SET {status_column} = {status} WHERE {column}= '{keyword}'"
        print(query)
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return False
    
    def insert_the_record(self, insert_column, insert_list):
        cursor = self.connection.cursor()
        print('insert list', insert_list)
        placeholder = ', '.join(['%s'] * len(insert_list))  # Assuming each sublist has one element
        query = f"INSERT IGNORE INTO {insert_column} (filingGuid) VALUES (%s)"
        print(query)
        insert_list = [(item,) for item in insert_list]
        print(insert_list)
        try:
            # Execute the query for multiple records
            cursor.executemany(query, insert_list)
            self.connection.commit()
            return True
        except Exception as e:
            print("Error:", e)
            self.connection.rollback()
            return False
        finally:
            cursor.close()




