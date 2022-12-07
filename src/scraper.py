from parsel import Selector
from typing import Optional, List
import json
import datetime

class Scraper:


    def create_html_tree(self, text: str) -> None:
        self.selector =  Selector(text=text)


    def title(self) -> Optional[str]:
            title = self.selector.xpath('//h1/text()').get()
            return title if title else None


    def price(self) -> Optional[int]:
        full_price = self.selector.xpath('//div[@class="price_value"]/strong/text()').get()
        if '$' in full_price:
            return int(full_price.replace('$', '').replace(' ', ''))
        else:
            prices = self.selector.xpath('//div[@class="price_value price_value--additional"]/text()').get()
            if prices:
                for price in prices:
                    if '$' in price:
                        return int(price.replace('$', '').replace(' ', ''))


    def mileage(self) -> Optional[int]:
        mileage = self.selector.xpath('//div[@class="base-information bold"]/span/text()').get()
        return int(mileage) * 1000 if mileage and mileage.isnumeric() else None


    def seller_title(self) -> Optional[str]:
        seller_title = self.selector.xpath('//div[contains(@class, "seller_info_title")]/text()').get()
        return seller_title.strip() if seller_title else None


    def seller_name(self) -> Optional[str]:
        name = self.selector.xpath('//div[contains(@class, "seller_info_name")]/text()').get()
        if not name:
            name = self.selector.xpath('//h4[contains(@class, "seller_info_name")]/a/text()').get()
        return name.strip() if name else None


    def seller_phones(self) -> List:
        phones = list()
        phones_div = self.selector.xpath('//div[contains(@class, "phones_list")]')
        if phones_div:
            for el in phones_div:
                phone = el.xpath('div/span[contains(@class, "phone")]/text()').get()
                if phone:
                    print('phone:', phone)
                    phones.append('+38' + phone.replace('(', '').replace(')', '').replace(' ', ''))
        return phones


    def main_image(self) -> Optional[str]:
        script = self.selector.xpath('//main/script/text()').get()
        if script:
            image = json.loads(script.strip().split('=')[-1])
            return image
        else:
            images = self.selector.xpath('//div[@class="image-gallery-slide center"]/div[contains(@class, "image-gallery-image")]/picture/source').attrib['srcset']
            return images.split(',')[-1].strip() if images else None


    def image_count(self) -> Optional[int]:
        counter_text = self.selector.xpath('//div[@class="action_disp_all_block"]/a/text()').get()
        if counter_text:
            for el in counter_text.split(' '):
                if el.isnumeric():
                    return int(el)


    def state_number(self) -> Optional[str]:
        number = self.selector.xpath('//span[contains(@class, "state-num")]/text()').get()
        return number.strip() if number else None


    def auto_data(self, url: str) -> dict:
        auto_data = dict(
            url = url,
            title = self.title(),
            price = self.price(),
            mileage = self.mileage(),
            seller_title = self.seller_title(),
            seller_name = self.seller_name(),
            seller_phones = self.seller_phones(),
            main_image = self.main_image(),
            image_count = self.image_count(),
            state_number = self.state_number(),
            vin_number = None,
            now = datetime.datetime.utcnow()
        )

        return auto_data


        

