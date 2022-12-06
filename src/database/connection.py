import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)  
sys.path.append(parent_directory)

import psycopg2
from dotenv import load_dotenv

load_dotenv()

POSTGRES_DB = os.environ.get('POSTGRES_DB')
DATABASE_URL = os.environ.get('DATABASE_URL')



class MyDatabase:
    
    def __init__(self) -> None:
        self.table_name = POSTGRES_DB
        self.conn = psycopg2.connect(DATABASE_URL)
        self.cursor = self.conn.cursor()
        

    def table_exists(self):
        try:
            self.cursor.execute(f'SELECT * FROM {self.table_name}')
            return True
        except psycopg2.errors.UndefinedTable:
            return False


    def create_table(self):
        self.cursor.execute(f"""CREATE TABLE {self.table_name} (
            id serial PRIMARY KEY,
            url varchar,
            title varchar,
            price integer,
            mileage integer,
            seller_title varchar,
            seller_name varchar,
            seller_phones varchar ARRAY,
            main_image varchar,
            image_count integer,
            state_number varchar,
            vin_number varchar,
            created_at timestamp
        )""")
        self.conn.commit()
    

if not MyDatabase().table_exists():
    MyDatabase().create_table()
    print('created')