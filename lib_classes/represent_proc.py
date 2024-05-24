class Representation:
    @staticmethod
    def print_news(news_items):
        for item in news_items:
            print(f"Rank: {item.rank}, Title: {item.title}, Score: {item.score}, Comments: {item.comments}")

    @staticmethod
    def write_news_to_file(news_items, file_name):
        with open(file_name, 'w') as file:
            for item in news_items:
                file.write(f"Rank: {item.rank}, Title: {item.title}, Score: {item.score}, Comments: {item.comments}\n")
