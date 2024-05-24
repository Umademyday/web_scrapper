import configparser
import requests
from bs4 import BeautifulSoup


class Configuration:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.url = self.config['SETTINGS']['URL']
        self.news_num = min(self.config.getint('SETTINGS', 'NEWS_NUM'), 30)
        self.words_num_filter1 = self.config.getint('SETTINGS', 'WORDS_NUM_FILTER1')
        self.words_num_filter2 = self.config.getint('SETTINGS', 'WORDS_NUM_FILTER2')
        self.news_items = self.fetch_and_parse_y_comb()

    def fetch_and_parse_y_comb(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        title_elements = soup.find_all("tr", class_="athing")
        subtext_elements = soup.find_all("td", class_="subtext")

        from lib_classes.data_proc import NewsFactory  # Import here to avoid circular imports
        news_items = [NewsFactory.create_from_soup(title_elements[i], subtext_elements[i]) for i in
                      range(self.news_num)]
        return news_items

    def __str__(self):
        return f"URL: {self.url}, NEWS_NUM: {self.news_num}, " \
               f"WORDS_NUM_FILTER1: {self.words_num_filter1}, WORDS_NUM_FILTER2: {self.words_num_filter2}"
