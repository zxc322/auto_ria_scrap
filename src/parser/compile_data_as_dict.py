import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)  
sys.path.append(parent_directory)

import datetime

from src.parser.auto_parser import AutoParser

class Compile:

    def __init__(self, auto_parser: AutoParser) -> None:
        self.auto_parser = auto_parser


    def auto_data(self) -> dict:
        auto_data = dict(
            url = self.auto_parser.auto_url,
            title = self.auto_parser.title(),
            price = self.auto_parser.price(),
            mileage = self.auto_parser.mileage(),
            seller_title = self.auto_parser.seller_title(),
            seller_name = self.auto_parser.seller_name(),
            seller_phones = self.auto_parser.seller_phones(),
            main_image = self.auto_parser.main_image(),
            image_count = self.auto_parser.image_count(),
            state_number = self.auto_parser.state_number(),
            vin_number = "TODO",
            now = datetime.datetime.utcnow()
        )

        return auto_data