import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)  
sys.path.append(parent_directory)

from typing import List
from src.database.connection import MyDatabase

class Insert(MyDatabase):

    def insert_auto(self, data_set: List[dict]):
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


    def auto_exists(self, url: str):
        self.cursor.execute(f""" 
            SELECT id FROM {self.table_name}
            WHERE url = '{url}' 
        """)
        return self.cursor.fetchone()