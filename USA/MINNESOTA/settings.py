import os
from dotenv import load_dotenv

load_dotenv()

# CORPORATIONS_URL = os.getenv("CORPORATIONS_URL")

AWS = {
    'access_key': os.getenv("AWS_ACCESS_KEY", None),
    'secret_key': os.getenv("AWS_SECRET_KEY", None),
    'region_name': os.getenv("AWS_REGION_NAME", None),
    'bucket': os.getenv("AWS_BUCKET", None),
    'source': os.getenv("AWS_SOURCE", None),
    'folder': os.getenv('AWS_FOLDER', None)
}

MYSQL = {
    'username': os.getenv('MYSQL_USERNAME', None),
    'password': os.getenv('MYSQL_PASSWORD', None),
    'url': os.getenv('MYSQL_URL', None),
    'port': int(os.getenv('MYSQL_PORT', None)),
    'schema': os.getenv('MYSQL_SCHEMA', None),
    'schema_mappings': os.getenv('MYSQL_SCHEMA_MAPPINGS', None),
    'table': os.getenv('MYSQL_TABLE', None),
    'procedure': os.getenv('MYSQL_PROCEDURE', None),
    'table_keyword': os.getenv('MYSQL_KEYWORD_TABLE', None),
    'procedure_keyword': os.getenv('MYSQL_KEYWORD_PROCEDURE', None),
    'procedure_parameter': os.getenv('MYSQL_PROCEDURE_PARAMETER', None)

}

SERVICE = {
    'queue': os.getenv('SERVICE_QUEUE', None),
    'name': os.getenv('SERVICE_NAME', None)
}

class JobStatus:
    CREATED = 1
    EXECUTING = 2
    FINISHED = 3
    ERROR = 4
