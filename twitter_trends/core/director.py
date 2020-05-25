import time, logging
from twitter_trends.settings import settings

class Director(object):

  def __init__(self, screen, trendsApi, renderer):
    self.screen = screen
    self.api = trendsApi
    self.renderer = renderer

  def run(self):
    trends = self.api.get_trends()
    for trend in trends:
      logging.info("Rendering trend: %s", trend.name)
      tweets = self.api.get_trend_tweets(trend, settings.TWITTER_TWEET_COUNT)
      self.screen.clear()
      self.__render_frame(self.renderer.render_trend(trend), settings.FLOW_TREND_DISPLAY_TIME)
      for tweet in tweets:
        logging.info("Rendering tweet author: %s", tweet.user)
        self.__render_frame(self.renderer.render_tweet_author(tweet), settings.FLOW_AUTHOR_DISPLAY_TIME)
        for textFrame in self.renderer.render_tweet_text(tweet):
          logging.info("Rendering tweet text frame")
          self.__render_frame(textFrame, settings.FLOW_TWEET_DISPLAY_TIME)
        for image in self.renderer.render_tweet_images(tweet):
          logging.info("Rendering tweet image")
          self.__render_frame(image, settings.FLOW_TWEET_IMAGE_DISPLAY_TIME)

  def __render_frame(self, image, duration):
    if image is None:
      return
    self.screen.render_frame(image)
    time.sleep(duration)
  