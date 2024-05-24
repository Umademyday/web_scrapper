class NewsFilter:
    def __init__(self, news_items, filter_mode):
        self.news_items = news_items
        self.filter_mode = filter_mode

    def filter(self, words_num_filter1, words_num_filter2):
        if self.filter_mode == 1:
            return sorted([item for item in self.news_items if item.words_count() > words_num_filter1],
                          key=lambda x: x.comments)
        elif self.filter_mode == 2:
            return sorted([item for item in self.news_items if item.words_count() <= words_num_filter2],
                          key=lambda x: x.score)
        else:
            return self.news_items


