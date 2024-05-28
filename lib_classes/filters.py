from abc import ABC, abstractmethod


class BaseFilter(ABC):
    @abstractmethod
    def apply(self, items):
        pass


class WordMinFilter(BaseFilter):
    def __init__(self, min_words):
        self.min_words = min_words

    def apply(self, items):
        return sorted([item for item in items if item.words_count() > self.min_words], key=lambda x: x.comments)


class WordMaxFilter(BaseFilter):
    def __init__(self, max_words):
        self.max_words = max_words

    def apply(self, items):
        return sorted([item for item in items if item.words_count() <= self.max_words], key=lambda x: x.score)