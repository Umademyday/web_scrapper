from dataclasses import dataclass


@dataclass
class NewsItem:
    rank: int
    title: str
    score: int
    comments: int


class NewsFactory:
    @staticmethod
    def create_from_soup(title_element, subtext_element) -> NewsItem:
        rank = int(title_element.find('span', class_="rank").text[:-1])
        title = title_element.find('span', class_="titleline").text

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
            score = 0
            comments = 0

        return NewsItem(rank=rank, title=title, score=score, comments=comments)