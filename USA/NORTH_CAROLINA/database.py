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
        
    def update_the_record(self, status, table, column, status_column, keyword):
        cursor = self.connection.cursor()
        query = f"UPDATE {table} SET {status_column} = {status} WHERE {column}= {keyword}"
        print(query)
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return False