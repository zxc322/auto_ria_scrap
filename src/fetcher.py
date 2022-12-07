import asyncio
import pyppeteer 
from typing import Optional

from src.scraper import Scraper
from src.database import Database

class Fetcher:

    def __init__(self, start_url: str = "https://auto.ria.com/uk/car/used/") -> None:
        self.start_url = start_url
        self.scraper = Scraper()


    async def run(self):
        browser = await pyppeteer.launch({"headless": False})
        page = await browser.newPage()
        await page.goto(self.start_url)
        await self.accept_cookies(page=page)

        while page:         
            print('[INFO] new page => ', page.url)
            page = await self.general_page_scrap(page)
        await browser.close()


    async def general_page_scrap(self, page: pyppeteer.page.Page):       
                
        urls_list = await page.querySelectorAll('div.item.ticket-title > a.address')
        urls_counter = len(urls_list)
        data_set = list()
        for i in range(urls_counter):          
            await asyncio.sleep(1)
            urls = await page.querySelectorAll('div.item.ticket-title > a')      
            print(f'[INFO] page progress: {i+1}/{urls_counter}')

            await asyncio.gather(
                page.waitForNavigation(),
                urls[i].click(selector='a'),
            )
            
            try:
                data = await self.scrap_auto_page(page=page)
                data_set.append(data)
            except pyppeteer.errors.PageError as ex:
                print(f'[ERROR] {ex}\nSkipping...')
      
            await page.goBack()
        
        Database().insert_auto(data_set=data_set)
        return await self.next_page(page)

    
    async def accept_cookies(self, page: pyppeteer.page.Page) -> None:
        cookies_btn = await page.querySelector('div.c-notifier-btns')
        if cookies_btn:
            await page.click('label.js-close.c-notifier-btn')

    
    async def next_page(self, page: pyppeteer.page.Page) -> Optional[pyppeteer.page.Page]:
        next_page_btn = await page.querySelector('a.js-next')
        if next_page_btn:
            await asyncio.gather(
                    page.waitForNavigation(),
                    next_page_btn.click(selector='a')
                )
            return page
        else:
            return None

    
    async def scrap_auto_page(self, page: pyppeteer.page.Page) -> dict:
        await asyncio.sleep(1)
        await page.click('a.phone_show_link')
        await asyncio.sleep(1)
        self.scraper.create_html_tree(text=await page.content())
        data = self.scraper.auto_data(url=page.url)
        await asyncio.sleep(1)
        return data