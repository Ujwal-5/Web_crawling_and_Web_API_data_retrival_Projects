import os

from dotenv import load_dotenv

load_dotenv()

# CORPORATIONS_URL = os.getenv("CORPORATIONS_URL")


MYSQL = {
    'username': os.getenv('MYSQL_USERNAME'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'url': os.getenv('MYSQL_URL'),
    'port': int(os.getenv('MYSQL_PORT')),
    'schema': os.getenv('MYSQL_SCHEMA'),
}

