import os
from typing import List
import psycopg2
from dotenv import load_dotenv

load_dotenv()

POSTGRES_DB = os.environ.get('POSTGRES_DB')
DOCKER_DATABASE_URL = os.environ.get('DOCKER_DATABASE_URL')
LOCAL_DATABASE_URL = os.environ.get('LOCAL_DATABASE_URL')

class Database:
    
    def __init__(self, docker_mode: bool = False) -> None:
        self.table_name = POSTGRES_DB
        db_url = LOCAL_DATABASE_URL if not docker_mode else DOCKER_DATABASE_URL
        self.conn = psycopg2.connect(db_url)
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

    
    def auto_exists(self, url: str):
        self.cursor.execute(f""" 
            SELECT id FROM {self.table_name}
            WHERE url = '{url}' 
        """)
        return self.cursor.fetchone()

        
    def insert_auto(self, data_set: List[dict]):
        print(f'[INFO] got dataset. Inserting data: {data_set}')
        for data in data_set:
            if not self.auto_exists(url=data['url']):
                self.cursor.execute(
                    f""" INSERT INTO {self.table_name} (
                        url, 
                        title, 
                        price, 
                        mileage, 
                        seller_title, 
                        seller_name, 
                        seller_phones, 
                        main_image, 
                        image_count, 
                        state_number, 
                        vin_number, 
                        created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",(
                        data['url'],
                        data['title'],
                        data['price'],
                        data['mileage'],
                        data['seller_title'],
                        data['seller_name'],
                        data['seller_phones'],
                        data['main_image'],
                        data['image_count'],
                        data['state_number'],
                        data['vin_number'],
                        data['now']
                    )
                )
        self.conn.commit()