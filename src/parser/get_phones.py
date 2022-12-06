import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)  
sys.path.append(parent_directory)

import httpx
import json

from src.constants.web import PHONE_URL, PHONE_URL_V2, HEADERS


class GetPhones:

    def __init__(self, client: httpx.Client) -> None:
        self.client = client
        

    def phones_by_GET(self, hash: str, expires: str, auto_id: str) -> list:
        phones = list()

        url = PHONE_URL + auto_id
        params = {
            "hash" : hash,
            "expires" : expires  
        }

        response = self.client.get(url=url, params=params)
        data = json.loads(response.text)
        for phone_dict in data.get('phones'):
            phone = phone_dict.get('phoneFormatted')
            if phone:
                phones.append('+38' + phone.replace('(', '').replace(')', '').replace(' ', ''))
        return phones

    
    def phones_by_POST(self, adv_id: int, phone_id: str) -> list:
        phones = list()
        url = PHONE_URL_V2
        data = dict(
            adv_id=adv_id,
            phone_id=phone_id,
            platform="desktop"
        )
        data = json.dumps(data)

        response = self.client.post(url=url, headers=HEADERS, data=data)
        if response.status_code==200:
            try:
                data = json.loads(response.text)
                phone = '+38' + data.get('phone')
                phones.append(phone)
                return phones
            except:
                return phones