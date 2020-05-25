import logging, yaml
from twitter_trends.core.models import SimpleTrend, SimpleTweet

class OfflineTrendsApi(object):

    def __init__(self, yaml_filename):
      with open(yaml_filename, "r") as yaml_file:
        yaml_string = yaml_file.read()
      self.trends = yaml.load(yaml_string)
      #for trend in self.trends:
      #  for tweet in trend.tweets:
      #    tweet.download_images()

    def get_trends(self):
        for trend in self.trends:
          yield trend

    def get_trend_tweets(self, trend, count):
      trend = self.__find_trend_by_name(trend.name)
      if trend == None:
        return
      for tweet in trend.tweets:
        tweet.download_images()
        yield tweet

    def __find_trend_by_name(self, trend_name):
      for trend in self.trends:
        if trend.name == trend_name:
          return trend
      return None
