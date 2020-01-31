import twitter, io, settings, requests
from datetime import date
from PIL import Image

class Api(object):

    def __init__(self):
        self.api = twitter.Api(consumer_key = settings.TWITTER_CONSUMER_KEY,
                                consumer_secret = settings.TWITTER_CONSUMER_SECRET,
                                access_token_key = settings.TWITTER_ACCESS_TOKEN_KEY,
                                access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET)

    def GetTrends(self):
        return self.api.GetTrendsWoeid(settings.TWITTER_WOEID)

    def GetTrendTweets(self, trend):
      today = date.today().strftime("%Y-%m-%d")
      return self.api.GetSearch(term = trend.query, result_type = "popular", since = today)

    def GetProfilePicture(self, tweet, full_size = True):
      profile_image_url = tweet.user.profile_image_url_https
      if full_size:
        profile_image_url = profile_image_url.replace("_normal", "")
      image_stream = requests.get(profile_image_url, stream = True)
      if image_stream.status_code == 200:
          return Image.open(io.BytesIO(image_stream.content))
      return None