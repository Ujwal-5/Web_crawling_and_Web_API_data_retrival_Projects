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
            DbService().get_a_record()


       
    def update_the_record(self, status, table, column, status_column, keyword, active_page, last_page):
        cursor = self.connection.cursor()
        query = f"UPDATE {table} SET {status_column} = {status}, ACTIVEPAGENO = '{active_page}', TOTALPAGENO = '{last_page}' WHERE {column}= '{keyword}'"
        print(query)
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return False
    
    def insert_the_record(self, insert_value):
        cursor = self.connection.cursor()
        print('insert value', insert_value)
        query = f"INSERT IGNORE INTO URL_PANAMA (folio_no) VALUES (%s)"
        print(query)
        try:
            # Execute the query for a single record
            cursor.execute(query, (insert_value,))
            self.connection.commit()
            return True
        except Exception as e:
            print("Error:", e)
            self.connection.rollback()
            return False
        finally:
            cursor.close()


    def is_value_present(self, check_value):
        cursor = self. connection.cursor()
        query = f"SELECT COUNT(*) FROM URL_PANAMA WHERE folio_no = %s"
        print(f"SELECT COUNT(*) FROM URL_PANAMA WHERE folio_no = '{check_value}'")
        try:
            cursor.execute(query, (check_value,))
            result = cursor.fetchone()
            print(result)
            return result[0] > 0
        except Exception as e:
            print("Error:", e)
            return False
        finally:
            cursor.close()