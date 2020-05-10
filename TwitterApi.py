import twitter, settings, html, ImageDownloadHelper
from datetime import date
from PIL import Image

class Api(object):

    def __init__(self):
        self.api = twitter.Api(consumer_key = settings.TWITTER_CONSUMER_KEY,
                                consumer_secret = settings.TWITTER_CONSUMER_SECRET,
                                access_token_key = settings.TWITTER_ACCESS_TOKEN_KEY,
                                access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET,
                                tweet_mode = settings.TWITTER_TWEET_MODE,
                                sleep_on_rate_limit = True)
        self.woeid = settings.TWITTER_WOEID
        self.fullSizeProfilePic = settings.TWITTER_FULL_SIZE_PROFILE_PIC

    def GetTrends(self):
        for trend in self.api.GetTrendsWoeid(self.woeid):
          yield Trend(trend)

    def GetTrendTweets(self, trend, count):
      today = date.today().strftime("%Y-%m-%d")
      for tweet in self.api.GetSearch(term = trend.query, count = count, result_type = "popular", since = today):
        yield Tweet(tweet, self.fullSizeProfilePic)

    def GetProfilePicture(self, tweet, full_size = True):
      profile_image_url = tweet.user.profile_image_url_https
      if full_size:
        profile_image_url = profile_image_url.replace("_normal", "")
      return ImageDownloadHelper.Download(profile_image_url)

    def GetImageAttachmentUrls(self, tweet):
      if tweet.media == None:
        return
      for m in tweet.media:
        if m.type == "photo":
          yield m.url


class Trend(object):

  def __init__(self, trend):
    self.name = trend.name
    self.query = trend.query

class Tweet(object):

  def __init__(self, tweet, full_size_profile_picture):
    tweet_mode = settings.TWITTER_TWEET_MODE
    self.user = u"@{0}".format(tweet.user.screen_name)
    self.text = self.__GetTweetText(tweet, tweet_mode)
    self.profile_pic = self.__GetProfilePicture(tweet.user.profile_image_url_https)
    self.images = self.__GetImages(tweet.media)

  def __GetProfilePicture(self, url, full_size = True):
      if full_size:
        url = url.replace("_normal", "")
      return ImageDownloadHelper.Download(url)

  def __GetImages(self, media):
      if media == None:
        return
      for m in media:
        if m.type == "photo":
          yield ImageDownloadHelper.Download(m.media_url_https)

  def __GetImageUrls(self, tweet):
      if tweet.media == None:
        return
      for m in tweet.media:
        if m.type == "photo":
          yield m.url

  def __GetTweetText(self, tweet, tweet_mode):
    text = ""
    if tweet_mode == "extended":
      text = tweet.full_text
    else:
      text = tweet.text

    for url in tweet.urls:
      text = text.replace(url.url, "")

    for url in self.__GetImageUrls(tweet):
      text = text.replace(url, "")

    text = text.replace(u"\n", u" ")
    text = text.replace(u"\r", u"")
    text = html.unescape(text)

    return text
