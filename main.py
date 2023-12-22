import requests
from typing import List
from bs4 import BeautifulSoup
import configparser

from lib_classes.data_proc import NewsItem
from lib_classes.data_proc import NewsFactory


config = configparser.ConfigParser()
config.read('config.ini')

URL = config['SETTINGS']['URL']
NEWS_NUM = min(config.getint('SETTINGS', 'NEWS_NUM'), 30)
WORDS_NUM_FILTER1 = config.getint('SETTINGS', 'WORDS_NUM_FILTER1')
WORDS_NUM_FILTER2 = config.getint('SETTINGS', 'WORDS_NUM_FILTER1')

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

title_elements = soup.find_all("tr", class_="athing")
subtext_elements = soup.find_all("td", class_="subtext")

news_items: List[NewsItem] = []

for i in range(NEWS_NUM):
    news_item = NewsFactory.create_from_soup(title_elements[i], subtext_elements[i])
    news_items.append(news_item)

# Example usage: printing the collected news items
for item in news_items:
    print(f"Rank: {item.rank}, Title: {item.title}, Score: {item.score}, Comments: {item.comments}")
