import os
import tweepy
import logging

LOGGER = logging.getLogger()

def create_api():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,)
    try:
        api.verify_credentials()
    except Exception as e:
        LOGGER.error("Error creating API", exc_info=True)
        raise e
    LOGGER.info("API created")

    return api