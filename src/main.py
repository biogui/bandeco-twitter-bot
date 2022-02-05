import os
import env
from apis_control import GIPHY_Control, Twitter_Control
from menu_control import Menu

SEARCH_TAG = 'hungry'
GIF_PATH   = 'temp.gif'

def main():
    # giphy_api_key          = os.getenv("GIPHY_API_KEY")
    # tt_consumer_key        = os.getenv("TT_CONSUMER_KEY")
    # tt_consumer_secret     = os.getenv("TT_CONSUMER_SECRET")
    # tt_access_token        = os.getenv("TT_ACCESS_TOKEN")
    # tt_access_token_secret = os.getenv("TT_ACCESS_TOKEN_SECRET")
    giphy_api_key          = env.GIPHY_API_KEY
    tt_consumer_key        = env.TT_CONSUMER_KEY
    tt_consumer_secret     = env.TT_CONSUMER_SECRET
    tt_access_token        = env.TT_ACCESS_TOKEN
    tt_access_token_secret = env.TT_ACCESS_TOKEN_SECRET

    giphy  = GIPHY_Control(giphy_api_key)
    tt_bot = Twitter_Control(
        tt_consumer_key,
        tt_consumer_secret,
        tt_access_token,
        tt_access_token_secret
    )
    menu   = Menu()

    menu.update_current_meal()
    giphy.download_random_gif(SEARCH_TAG, GIF_PATH)

    tt_bot.post_tweet(menu.current_meal, GIF_PATH)
    os.remove(GIF_PATH)

if __name__ == '__main__':
    print('Bot is running...')
    main()
    print('Bot shut down!')