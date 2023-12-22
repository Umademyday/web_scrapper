import requests
from bs4 import BeautifulSoup
import configparser
import argparse

from lib_classes.data_proc import NewsFactory

parser = argparse.ArgumentParser(description='Filter and output news items.')

# Adding arguments
parser.add_argument('--filtering_mode', type=int, choices=[1, 2], default=0,
                    help='Filtering mode: 1 or 2 (no filtering if not specified)')
parser.add_argument('--outputfile_name', type=str, default='',
                    help='Output file name (if specified, output to the file)')

# Parse and access the arguments
args = parser.parse_args()
filtering_mode = args.filtering_mode
outputfile_name = args.outputfile_name

# Parse configfile
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

if __name__ == '__main__':
    # Create news using Factory
    news_items = [NewsFactory.create_from_soup(title_elements[i], subtext_elements[i]) for i in range(NEWS_NUM)]

    # Now filter according to args
    if filtering_mode == 1:
        print('Filtering mode 1 enabled')
        news_items = sorted([x for x in news_items if x.words_count() > WORDS_NUM_FILTER1], key=lambda x: x.comments)

    elif filtering_mode == 2:
        print('Filtering mode 2 enabled')
        news_items = sorted([x for x in news_items if x.words_count() <= WORDS_NUM_FILTER2], key=lambda x: x.score)

    # Print to file
    if outputfile_name:
        with open(outputfile_name, 'w') as file:
            for item in news_items:
                file.write(f"Rank: {item.rank}, Title: {item.title}, Score: {item.score}, Comments: {item.comments}\n")
    # Print to stdout
    else:
        for item in news_items:
            print(f"Rank: {item.rank}, Title: {item.title}, Score: {item.score}, Comments: {item.comments}")
