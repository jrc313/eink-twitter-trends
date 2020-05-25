import twitter, settings, logging
from datetime import date
from twitter_trends.models import SimpleTrend, SimpleTweet

class TrendsApi(object):

    def __init__(self):
        self.api = twitter.Api(consumer_key = settings.TWITTER_CONSUMER_KEY,
                                consumer_secret = settings.TWITTER_CONSUMER_SECRET,
                                access_token_key = settings.TWITTER_ACCESS_TOKEN_KEY,
                                access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET,
                                tweet_mode = settings.TWITTER_TWEET_MODE,
                                sleep_on_rate_limit = True)
        self.woeid = settings.TWITTER_WOEID
        

    def get_trends(self):
        for trend in self.api.GetTrendsWoeid(self.woeid):
          yield SimpleTrend.from_trend(trend)

    def get_trend_tweets(self, trend, count):
      today = date.today().strftime("%Y-%m-%d")
      for tweet in self.api.GetSearch(term = trend.query, count = count, result_type = "popular", since = today):
        yield SimpleTweet.from_tweet(tweet)