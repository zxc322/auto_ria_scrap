import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)  
sys.path.append(parent_directory)

from typing import Optional
import httpx
import json

from src.parser.generic import Generic
from src.parser.get_phones import GetPhones


class AutoParser(Generic):
    
    def __init__(self, text: str, url: str, client: httpx.Client) -> None:
        super().__init__(text)
        self.auto_url = url
        self.client = client


    def title(self) -> Optional[str]:
        try:
            title = self.selector.xpath('//h1/text()').get()
            return title
        except:
            return None


    def price(self) -> Optional[int]:
        try:
            full_price = self.selector.xpath('//div[@class="price_value"]/strong/text()').get()
            if '$' in full_price:
                return int(full_price.replace('$', '').replace(' ', ''))
            else:
                prices = self.selector.xpath('//div[@class="price_value price_value--additional"]/text()').get()
                for price in prices:
                    if '$' in price:
                        return int(price.replace('$', '').replace(' ', ''))
        except:
            return None

    
    def mileage(self) -> Optional[int]:
        try:
            mileage = self.selector.xpath('//div[@class="base-information bold"]/span/text()').get()
            return int(mileage) * 1000
        except:
            return None


    def seller_title(self) -> Optional[str]:
        try:
            seller_title = self.selector.xpath('//div[contains(@class, "seller_info_title")]/text()').get().strip()
            return seller_title
        except:
            return None


    def seller_name(self) -> Optional[str]:
        try:
            name = self.selector.xpath('//div[contains(@class, "seller_info_name")]/text()').get()
            if not name:
                name = self.selector.xpath('//h4[contains(@class, "seller_info_name")]/a/text()').get()
            return name.strip()
        except:
            return None


    def seller_phones(self) -> list:
        try:
            get_phones = GetPhones(client=self.client)
            user_data = self.selector.xpath('//script[contains(@class, "js-user-secure")]')
            auto_id = self.auto_url.split('_')[-1].replace('.html', '')
            hash = user_data.attrib['data-hash']
            expires = user_data.attrib['data-expires']
            phones = get_phones.phones_by_GET(hash=hash, auto_id=auto_id, expires=expires)
            return phones
        except:
            try:
                phones = get_phones.phones_by_POST(adv_id=int(auto_id), phone_id=self.get_phone_id())
                return phones
            except:
                return list()


    def get_phone_id(self) -> Optional[int]:
        """ We are looking for this field in script ("phone_id":"680971717") """

        scripts = self.selector.xpath('//script').getall()
        for s in scripts:
            idx = s.find('phone_id')
            if idx > 0:
                phone_id = ''
                for number in s[idx+11:]:
                    if number.isnumeric():
                        phone_id += number
                    else:
                        break
        return phone_id


    def main_image(self) -> Optional[str]:
        try:
            script = self.selector.xpath('//main/script/text()').get().strip()
            image = json.loads(script.split('=')[-1])
            return image
        except:
            try:
                images = self.selector.xpath('//div[@class="image-gallery-slide center"]/div[contains(@class, "image-gallery-image")]/picture/source').attrib['srcset']
                image = images.split(',')[-1].strip()
                return image
            except:
                return None


    def image_count(self) -> Optional[int]:
        try:
            counter_text = self.selector.xpath('//div[@class="action_disp_all_block"]/a/text()').get()
            for el in counter_text.split(' '):
                if el.isnumeric():
                    counter = int(el)
                    break
            return counter
        except:
            return None


    def state_number(self) -> Optional[str]:
        try:
            number = self.selector.xpath('//span[contains(@class, "state-num")]/text()').get().strip()
            return number
        except:
            return None
