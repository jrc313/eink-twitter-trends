import twitter, logging
from datetime import date, timedelta
from twitter_trends.settings import settings
from twitter_trends.core.models import SimpleTrend, SimpleTweet

class TrendsApi(object):

    def __init__(self):
        self.api = twitter.Api(consumer_key = settings.TWITTER_CONSUMER_KEY,
                                consumer_secret = settings.TWITTER_CONSUMER_SECRET,
                                access_token_key = settings.TWITTER_ACCESS_TOKEN_KEY,
                                access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET,
                                tweet_mode = settings.TWITTER_TWEET_MODE,
                                sleep_on_rate_limit = True)
        self.woeid = settings.TWITTER_WOEID
        self.tweet_days = settings.TWITTER_TWEET_AGE_DAYS
        

    def get_trends(self):
        for trend in self.api.GetTrendsWoeid(self.woeid):
          yield SimpleTrend.from_trend(trend)

    def get_trend_tweets(self, trend, count):
      search_since = date.today() - timedelta(days = self.tweet_days)
      search_since_string = search_since.strftime("%Y-%m-%d")
      for tweet in self.api.GetSearch(term = trend.query, count = count, result_type = "popular", since = search_since_string):
        yield SimpleTweet.from_tweet(tweet)