import configparser


class Configuration:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.url = self.config['SETTINGS']['URL']
        self.news_num = min(self.config.getint('SETTINGS', 'NEWS_NUM'), 30)
        self.words_num_filter1 = self.config.getint('SETTINGS', 'WORDS_NUM_FILTER1')
        self.words_num_filter2 = self.config.getint('SETTINGS', 'WORDS_NUM_FILTER2')

    def __str__(self):
        return f"URL: {self.url}, NEWS_NUM: {self.news_num}, " \
               f"WORDS_NUM_FILTER1: {self.words_num_filter1}, WORDS_NUM_FILTER2: {self.words_num_filter2}"
