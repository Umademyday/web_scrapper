from abc import ABC, abstractmethod


class BaseFilter(ABC):
    @abstractmethod
    def apply(self, items):
        pass


class LenFilter(BaseFilter):
    def __init__(self, news_num):
        self.news_num = news_num

    def apply(self, items):
        return items[:self.news_num]


class WordMinFilter(BaseFilter):
    def __init__(self, min_words, news_num):
        self.min_words = min_words
        self.news_num = news_num

    def apply(self, items):
        return sorted([item for item in items if item.words_count() > self.min_words],
                      key=lambda x: x.comments)[:self.news_num]


class WordMaxFilter(BaseFilter):
    def __init__(self, max_words, news_num):
        self.max_words = max_words
        self.news_num = news_num

    def apply(self, items):
        return sorted([item for item in items if item.words_count() <= self.max_words],
                      key=lambda x: x.score)[:self.news_num]
