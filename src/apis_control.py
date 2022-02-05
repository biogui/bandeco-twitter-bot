import random
import tweepy
import requests
import giphy_client

class Twitter_Control:
    def __init__(
            self, consumer_key, consumer_secret,
            access_token, access_token_secret
        ):
        self.consumer_key        = consumer_key
        self.consumer_secret     = consumer_secret
        self.access_token        = access_token
        self.access_token_secret = access_token_secret

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth)

    def post_tweet(self, text, img_path=None):
        if img_path:
            self.api.update_status_with_media(text, img_path)
        else:
            self.api.update_status(text)

class GIPHY_Control:
    def __init__(self, api_key):
        self.api     = giphy_client.DefaultApi()
        self.api_key = api_key

        self.lasted_gif = None

    def download_random_gif(self, searched_tag, download_path):
        r = self.api.gifs_search_get(
            self.api_key, searched_tag,
            offset=random.randint(1, 50), fmt='gif'
        )
        gif = random.choice(r.data)
        gif_url = gif.images.downsized.url

        content = requests.get(gif_url).content
        with open(download_path,'wb') as f:
            f.write(content)