import argparse
import logging
import sys
from requests.exceptions import RequestException


from lib_classes.config_proc import Configuration
from lib_classes.parcer_proc import Parser
from lib_classes.filter_proc import NewsFilter
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

        # Fetch and parse news
        parser = Parser(config.url, config.news_num)
        news_items = parser.news_items

        # Filter news items
        if filtering_mode not in [0, 1, 2]:
            logging.error('Wrong filtering attribute')
        news_filter = NewsFilter(news_items, filtering_mode)

        logging.info('Starting filtering')
        news_items = news_filter.filter(config.words_num_filter1, config.words_num_filter2)

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
