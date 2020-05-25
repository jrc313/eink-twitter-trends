import io, requests, logging, html
from PIL import Image
from twitter_trends.settings import settings

class SimpleTrend(object):

  def __init__(self):
    self.name = ""
    self.query = ""
  
  @staticmethod
  def from_trend(trend):
    simple_trend = SimpleTrend()
    simple_trend.name = trend.name
    simple_trend.query = trend.query
    return simple_trend

class SimpleTweet(object):

  def __init__(self):
    self.fullSizeProfilePic = settings.TWITTER_FULL_SIZE_PROFILE_PIC

  @staticmethod
  def from_tweet(tweet):
    simple_tweet = SimpleTweet()
    simple_tweet.init_from_tweet(tweet)
    return simple_tweet

  def init_from_tweet(self, tweet):
    tweet_mode = settings.TWITTER_TWEET_MODE
    self.profile_pic_url = self.__get_profile_picture_url(tweet.user.profile_image_url_https)
    self.image_urls = self.__get_image_urls(tweet)
    self.user = u"@{0}".format(tweet.user.screen_name)
    self.text = self.__get_tweet_text(tweet, tweet_mode)
    self.download_images()

  def download_images(self):
    self.profile_pic = self.__get_profile_picture(self.profile_pic_url)
    self.images = self.__get_images()

  def __get_profile_picture_url(self, url):
    if self.fullSizeProfilePic:
      url = url.replace("_normal", "")
    return url

  def __get_image_urls(self, tweet):
      if tweet.media == None:
        return
      for m in tweet.media:
        if m.type == "photo":
          yield m.url

  def __get_profile_picture(self, url):
    return ImageDownloadHelper.download(url)

  def __get_images(self):
    for u in self.image_urls:
      yield ImageDownloadHelper.download(u)

  def __get_tweet_text(self, tweet, tweet_mode):
    text = ""
    if tweet_mode == "extended":
      text = tweet.full_text
    else:
      text = tweet.text

    for url in tweet.urls:
      text = text.replace(url.url, "")

    for url in self.image_urls:
      text = text.replace(url, "")

    text = text.replace(u"\n", u" ")
    text = text.replace(u"\r", u"")
    text = html.unescape(text)

    return text


class ImageDownloadHelper(object):

  @staticmethod
  def download(url):
    logging.debug("Downloading image: {0}".format(url))
    image_stream = requests.get(url, stream = True)
    if image_stream.status_code == 200:
      logging.debug("Download success")
      try:
        return Image.open(io.BytesIO(image_stream.content))
      except Exception as e:
        logging.debug("Failed to open image: {0}".format(e))
        return ImageDownloadHelper.get_fail_image()

  @staticmethod
  def get_fail_image():
    filename = settings.FAIL_IMAGE_FILENAME
    return Image.open(filename)