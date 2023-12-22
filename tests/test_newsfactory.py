import unittest
from bs4 import BeautifulSoup
from lib_classes.data_proc import NewsFactory, NewsItem


class TestNewsFactory(unittest.TestCase):
    def setUp(self):
        # Example HTML content
        with open('test_data/example.html', 'r', encoding='utf-8') as file:
            example_html = file.read()

        self.soup = BeautifulSoup(example_html, "html.parser")
        self.title_element = self.soup.find("tr", class_="athing")
        self.subtext_element = self.soup.find("td", class_="subtext")

    def test_create_from_soup(self):
        news_item = NewsFactory.create_from_soup(self.title_element, self.subtext_element)
        # print(news_item)
        self.assertIsInstance(news_item, NewsItem)
        self.assertEqual(news_item.score, 92)
        self.assertEqual(news_item.rank, 1)
        self.assertEqual(news_item.title, 'From Nand to Tetris: Building a Modern Computer from First Principles')
        self.assertEqual(news_item.comments, 25)


class TestNewsItem(unittest.TestCase):
    def test_words_count(self):
        # Assuming a NewsItem object and a title
        news_item = NewsItem(rank=1, title="Example Title NUM-TWO dot.com", score=1, comments=1)
        words_count = news_item.words_count()
        self.assertEqual(words_count, 5)


if __name__ == '__main__':
    unittest.main()