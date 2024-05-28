import argparse
import logging
import sys
from requests.exceptions import RequestException


from lib_classes.config_proc import Configuration
from lib_classes.data_sources import URLDataSource
from lib_classes.parsers import YcombHTMLParser
from lib_classes.data_proc import NewsFactory
from lib_classes.filters import WordMaxFilter, WordMinFilter
from lib_classes.represent_proc import Representation


def main():
    # Configuring logs
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Starting configuration gathering')

    parser = argparse.ArgumentParser(description='Filter and output news items.')

    # Adding arguments
    parser.add_argument('--filtering_mode', type=int, choices=[1, 2], default=0,
                        help='Filtering mode: 1 or 2 (no filtering if not specified)')
    parser.add_argument('--outputfile_name', type=str, default='',
                        help='Output file name (if specified, output to the file)')

    # Parsing and accessing the arguments
    args = parser.parse_args()
    filtering_mode = args.filtering_mode
    outputfile_name = args.outputfile_name

    try:
        logging.info('Fetching news')

        # Load configuration and fetch news
        config = Configuration('config.ini')
        data_source = URLDataSource(config.url)

        # Fetch and parse news
        content = data_source.fetch()
        parser = YcombHTMLParser(config.url)

        # Parse data
        parsed_data = parser.parse(content)
        title_elements, subtext_elements = parsed_data

        # Convert parsed data to NewsItem objects
        news_items = [NewsFactory.create_from_soup(title_elem, subtext_elem) for title_elem, subtext_elem in
                      zip(title_elements, subtext_elements)]

        # Filter news items
        logging.info('Starting filtering')
        if filtering_mode == 1:
            news_filter = WordMinFilter(min_words=config.words_num_filter1)
        elif filtering_mode == 2:
            news_filter = WordMaxFilter(max_words=config.words_num_filter2)
        else:
            news_filter = None

        if news_filter:
            news_items = news_filter.apply(news_items)

        # Output the results
        if outputfile_name:
            logging.info(f'Writing data to {outputfile_name}')
            Representation.write_news_to_file(news_items, outputfile_name)
        else:
            Representation.print_news(news_items)

        logging.info('Execution completed.')

    except FileNotFoundError as e:
        logging.error(f'Configuration file not found: {e}')
        sys.exit(1)
    except RequestException as e:
        logging.error(f'Network error while fetching news: {e}')
        sys.exit(1)
    except Exception as e:
        logging.error(f'An unexpected error occurred: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
