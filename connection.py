import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()

class PostgreSQLConnection:

    def __init__(self):
        self.db_config = {
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host':  os.getenv('DB_HOST'),
            'port':  os.getenv('DB_PORT') 
        }

    def connect(self):
        try:
            self.connection = psycopg2.connect(**self.db_config)
            # print('*CONEXION EXITOSA (PostgreSQL)*')
            return self.connection
        except Exception as e:
            print(f'*ERROR CONEXION (PostgreSQL): {e}*')
            return False
        finally:
            self.connection = None
        
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print('*CONEXION CERRADA (PostgreSQL)*')
