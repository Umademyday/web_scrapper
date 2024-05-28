from bs4 import BeautifulSoup
from abc import ABC, abstractmethod


class BaseParser(ABC):
    @abstractmethod
    def parse(self, content):
        pass


class YcombHTMLParser(BaseParser):
    def __init__(self, url):
        self.url = url
        # self.news_num = news_num
        # self.news_items = self.parse()

    def parse(self, content):

        soup = BeautifulSoup(content, "html.parser")
        title_elements = soup.find_all("tr", class_="athing")
        subtext_elements = soup.find_all("td", class_="subtext")

        return title_elements, subtext_elements


class JSONParser(BaseParser):
    def parse(self, content):
        # Implementation for parsing JSON content
        pass
