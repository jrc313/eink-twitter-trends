import os
from dotenv import load_dotenv
import confuse

# Load secrets from environment
load_dotenv()

TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN_KEY = os.getenv("TWITTER_ACCESS_TOKEN_KEY")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Load general settings from settings.yml

config = confuse.Configuration("TwitterTrends", __name__)

TWITTER_WOEID = config["twitter"]["woeid"].get(int)

RENDERER_ASSET_PATH = config["renderer"]["asset_path"].get()
RENDERER_TREND_FONT_NAME = config["renderer"]["trend_font"].get()
RENDERER_TREND_FONT_SIZE = config["renderer"]["trend_font_size"].get(int)
RENDERER_HANDLE_FONT_NAME = config["renderer"]["handle_font"].get()
RENDERER_HANDLE_FONT_SIZE = config["renderer"]["handle_font_size"].get(int)
RENDERER_TWEET_FONT_NAME = config["renderer"]["tweet_font"].get()
RENDERER_TWEET_FONT_SIZE = config["renderer"]["tweet_font_size"].get(int)
RENDERER_PADDING = config["renderer"]["padding"].get(int)
RENDERER_PROFILE_IMAGE_SIZE = config["renderer"]["profile_image_size"].get(int)