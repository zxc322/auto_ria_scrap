import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)  
sys.path.append(parent_directory)

import httpx
from src.parser.urls_parser import UrlParser
from src.parser.auto_parser import AutoParser
from src.parser.compile_data_as_dict import Compile
from src.database.insert import Insert

class Fetcher:

    # def __init__(self) -> None:
    #     self.client = httpx.Client()

    def run_scrap(self, url: str):
        with httpx.Client() as client:
            response = client.get(url)
            url_parser = UrlParser(text=response.text)
            urls = url_parser.get_urls_list()
            self.auto_scrap(urls=urls)
            return url_parser.next_page()

     
    def auto_scrap(self, urls: list):
        with httpx.Client() as client:
            data_set = list()
            for url in urls:
                response = client.get(url)
                print(f'[INFO] url: {url}, status: {response.status_code}')
                auto_parser = AutoParser(text=response.text, url=url, client=client)
                compilator = Compile(auto_parser=auto_parser)
                data_set.append(compilator.auto_data())
            print(data_set)
            Insert().insert_auto(data_set=data_set)

    
    
