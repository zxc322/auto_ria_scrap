from parsel import Selector


class Generic:

    def __init__(self, text) -> None:
        self.selector = Selector(text=text)