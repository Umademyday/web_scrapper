from dataclasses import dataclass
import re


@dataclass
class NewsItem:
    rank: int
    title: str
    score: int
    comments: int

    def words_count(self):
        url_pattern = r'\b(?:https?://|www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+)\b'

        title_without_spec = re.sub(url_pattern, 'link', self.title)
        title_without_spec = title_without_spec.replace('-', ' ')

        return len(re.findall(r'\S+', title_without_spec))


class NewsFactory:
    @staticmethod
    def create_from_soup(title_element, subtext_element) -> NewsItem:
        rank = int(title_element.find('span', class_="rank").text[:-1])
        title = title_element.find('span', class_="titleline").find('a', href=True).text

        try:
            score = int(subtext_element.find('span', class_="score").text.split()[0])
            comments_text = subtext_element.find_all('a', href=True)[-1].text

            if comments_text == 'discuss':
                comments = 0
            elif 'comment' in comments_text:
                comments = int(comments_text.split()[0])
            else:
                comments = 0

        except AttributeError:
            # Sometimes news do not have substring, so we put score and comments to 0
            score = 0
            comments = 0

        return NewsItem(rank=rank, title=title, score=score, comments=comments)
