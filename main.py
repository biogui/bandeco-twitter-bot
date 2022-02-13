import os
from datetime import datetime
from src.apis_control import GIPHY_Control, Twitter_Control
from src.menu_control import Menu

GIF_PATH = 'temp.gif'

def main():
    giphy_api_key          = os.getenv("GIPHY_API_KEY")
    tt_consumer_key        = os.getenv("TT_CONSUMER_KEY")
    tt_consumer_secret     = os.getenv("TT_CONSUMER_SECRET")
    tt_access_token        = os.getenv("TT_ACCESS_TOKEN")
    tt_access_token_secret = os.getenv("TT_ACCESS_TOKEN_SECRET")

    giphy  = GIPHY_Control(giphy_api_key)
    tt_bot = Twitter_Control(
        tt_consumer_key,
        tt_consumer_secret,
        tt_access_token,
        tt_access_token_secret
    )
    menu   = Menu()

    menu.update_current_meal()
    print(menu.current_meal)

    giphy.download_random_gif(menu.current_meal.gif_tag, GIF_PATH)

    tt_bot.post_tweet(menu.current_meal, GIF_PATH)
    os.remove(GIF_PATH)

if __name__ == '__main__':
    print(f'Bot is running [{datetime.now()}]...')
    main()
    print('Bot shut down!')