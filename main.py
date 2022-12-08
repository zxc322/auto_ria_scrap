import asyncio
import sys, os

from src.fetcher import Fetcher
from src.database import Database


docker_mode=True

if not Database(docker_mode=docker_mode).table_exists():
    Database(docker_mode=docker_mode).create_table()

start_url="https://auto.ria.com/uk/car/used/?page=12"

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(Fetcher(docker_mode=docker_mode).run())
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)