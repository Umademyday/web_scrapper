import argparse
import logging

from lib_classes.config_proc import Configuration
from lib_classes.filter_proc import NewsFilter
from lib_classes.represent_proc import Representation

if __name__ == '__main__':

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
    logging.info('Fetching news')

    # Load configuration and fetch news
    config = Configuration()
    news_items = config.news_items

    # Filter news items
    news_filter = NewsFilter(news_items, filtering_mode)
    if filtering_mode not in [0, 1, 2]:
        logging.error('Wrong filtering attribute')

    logging.info('Starting filtering')
    news_items = news_filter.filter(config.words_num_filter1, config.words_num_filter2)

    # Output the results
    if outputfile_name:
        logging.info(f'Writing data to {outputfile_name}')
        Representation.write_news_to_file(news_items, outputfile_name)
    else:
        Representation.print_news(news_items)

    logging.info('Execution completed.')
