from src.scraper.start_fetching import Fetcher
from src.constants.web import URL as url
from src.database.connection import MyDatabase

import time
import sys

if not MyDatabase().table_exists():
    MyDatabase().create_table()

if len(sys.argv)>1:
    url = sys.argv[1]

fetcher = Fetcher()
page_counter = 1

if __name__ == '__main__':
    start = time.time()
    while url:
        print(f'--- page-{page_counter}, url: {url}, current_time: {time.time()-start} ---', end='\n')
        url = fetcher.run_scrap(url)
        page_counter += 1





