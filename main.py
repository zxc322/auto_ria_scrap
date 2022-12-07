import asyncio

from src.fetcher import Fetcher
from src.database import Database




if not Database().table_exists():
    Database().create_table()


# start_url="https://auto.ria.com/uk/car/used/?page=12"
asyncio.get_event_loop().run_until_complete(Fetcher().run())


