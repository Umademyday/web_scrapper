import unittest
from bs4 import BeautifulSoup
from unittest.mock import patch, Mock

from lib_classes.data_proc import NewsFactory, NewsItem
from lib_classes.parsers import YcombHTMLParser


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
        self.assertIsInstance(news_item, NewsItem)
        self.assertEqual(news_item.score, 92)
        self.assertEqual(news_item.rank, 1)
        self.assertEqual(news_item.title, 'From Nand to Tetris: Building a Modern Computer from First Principles')
        self.assertEqual(news_item.comments, 25)

    def test_words_count(self):
        # Assuming a NewsItem object and a title
        news_item = NewsItem(rank=1, title="Example Title NUM-TWO dot.com", score=1, comments=1)
        words_count = news_item.words_count()
        self.assertEqual(words_count, 5)


class TestYcombHTMLParser(unittest.TestCase):
    def setUp(self):
        # Example HTML content
        with open('test_data/example.html', 'r', encoding='utf-8') as file:
            self.sample_html = file.read()
        self.parser = YcombHTMLParser(url="https://news.ycombinator.com/")

    @patch('requests.get')
    def test_parse(self, mock_get):
        # Mock the HTTP response
        mock_response = Mock()
        mock_response.content = self.sample_html
        mock_get.return_value = mock_response

        # Fetch the content (using the mocked response)
        response = mock_get(self.parser.url)
        content = response.content

        # Parse the content
        title_elements, subtext_elements = self.parser.parse(content)
        news_items = [NewsFactory.create_from_soup(title_elem, subtext_elem) for title_elem, subtext_elem in
                      zip(title_elements, subtext_elements)]
        # Assertions
        self.assertEqual(len(title_elements), 30)
        self.assertEqual(len(subtext_elements), 30)

        # Check the content of the first news item
        self.assertEqual(len(news_items), 30)
        self.assertEqual(news_items[0].rank, 1)
        self.assertEqual(news_items[0].title,
                         '''From Nand to Tetris: Building a Modern Computer from First Principles''')
        self.assertEqual(news_items[0].score, 92)
        self.assertEqual(news_items[0].comments, 25)


if __name__ == '__main__':
    unittest.main()
