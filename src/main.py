from api_control  import create_api
from menu_control import LOGGER, MenuScraper

def main():
    bot = create_api()
    menu = MenuScraper()

    menu.update_current_meal()

    bot.update_status(menu.current_meal)

if __name__ == '__main__':
    LOGGER.info('Bot is running...')
    main()
    LOGGER.info('Bot shut down!')