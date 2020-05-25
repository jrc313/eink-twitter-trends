import os
from dotenv import load_dotenv
import confuse

load_dotenv()
config = confuse.Configuration("TwitterTrends", __name__)

class settings:
  # Load secrets from environment
  TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
  TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
  TWITTER_ACCESS_TOKEN_KEY = os.getenv("TWITTER_ACCESS_TOKEN_KEY")
  TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

  # Load general settings from settings.yml
  TWITTER_WOEID = config["twitter"]["woeid"].get(int)
  TWITTER_TWEET_COUNT = config["twitter"]["tweet_count"].get(int)
  TWITTER_TWEET_MODE = config["twitter"]["tweet_mode"].get()
  TWITTER_FULL_SIZE_PROFILE_PIC = config["twitter"]["full_size_profile_pic"].get(bool)
  TWITTER_TWEET_AGE_DAYS = config["twitter"]["tweet_age_days"].get(int)

  FLOW_TREND_DISPLAY_TIME = config["flow"]["trend_display_time"].get(int)
  FLOW_AUTHOR_DISPLAY_TIME = config["flow"]["author_display_time"].get(int)
  FLOW_TWEET_DISPLAY_TIME = config["flow"]["tweet_display_time"].get(int)
  FLOW_TWEET_IMAGE_DISPLAY_TIME = config["flow"]["tweet_image_display_time"].get(int)

  RENDERER_ASSET_PATH = config["renderer"]["asset_path"].get()
  RENDERER_TREND_FONT_NAME = config["renderer"]["trend_font"].get()
  RENDERER_TREND_FONT_SIZE = config["renderer"]["trend_font_size"].get(int)
  RENDERER_HANDLE_FONT_NAME = config["renderer"]["handle_font"].get()
  RENDERER_HANDLE_FONT_SIZE = config["renderer"]["handle_font_size"].get(int)
  RENDERER_TWEET_FONT_NAME = config["renderer"]["tweet_font"].get()
  RENDERER_TWEET_FONT_SIZE = config["renderer"]["tweet_font_size"].get(int)
  RENDERER_PADDING = config["renderer"]["padding"].get(int)
  RENDERER_PROFILE_IMAGE_SIZE = config["renderer"]["profile_image_size"].get(int)
  RENDERER_TWEET_TEXT_WIDTH = config["renderer"]["tweet_text_width"].get(int)
  RENDERER_TEXT_SCROLL_SPEED = config["renderer"]["text_scroll_speed"].get(float)

  FAIL_IMAGE_FILENAME = config["renderer"]["fail_image_filename"].get()