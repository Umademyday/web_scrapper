import requests
from bs4 import BeautifulSoup
from lib_classes.data_proc import NewsFactory


class Parser:
    def __init__(self, url, news_num):
        self.url = url
        self.news_num = news_num
        self.news_items = self._fetch_and_parse_news()

    def _fetch_and_parse_news(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        title_elements = soup.find_all("tr", class_="athing")
        subtext_elements = soup.find_all("td", class_="subtext")
        news_items = [NewsFactory.create_from_soup(title_elements[i], subtext_elements[i]) for i in range(self.news_num)]
        return news_items
