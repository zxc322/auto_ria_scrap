import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)  
sys.path.append(parent_directory)

from src.parser.generic import Generic

class UrlParser(Generic):
    
    def __init__(self, text) -> None:
        super().__init__(text)

    
    def get_urls_list(self):
        return (url.attrib['href'] for url in self.selector.xpath('//div[@class="item ticket-title"]/a'))


    def next_page(self):
        try:
            next_page = self.selector.xpath('//a[@class="page-link js-next "]').attrib['href']
            return next_page
        except:
            return None
