from config import LOGGER, create_api
from menu import Scraper

def main():
    bot = create_api()

    schedule.every(2).seconds.do(printgamer)

    while True:
        schedule.run_pending()

if __name__ == '__main__':
    LOGGER.info('Bot is running...')
    main()
    LOGGER.info('Bot shut down!')