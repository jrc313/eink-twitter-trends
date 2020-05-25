import PIL
from PIL import Image, ImageDraw, ImageFont, ImageOps
import textwrap, os


import settings

MAX_COLOUR = 255
IMAGE_MODE = "1"

class ImageRenderer(object):

  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.__load_fonts()
    self.__init_props()

  def __load_fonts(self):
    self.trend_font = ImageFont.truetype(
      os.path.join(settings.RENDERER_ASSET_PATH, settings.RENDERER_TREND_FONT_NAME),
      settings.RENDERER_TREND_FONT_SIZE)
    self.handle_font = ImageFont.truetype(
      os.path.join(settings.RENDERER_ASSET_PATH, settings.RENDERER_HANDLE_FONT_NAME),
      settings.RENDERER_HANDLE_FONT_SIZE)
    self.tweet_font = ImageFont.truetype(
      os.path.join(settings.RENDERER_ASSET_PATH, settings.RENDERER_TWEET_FONT_NAME),
      settings.RENDERER_TWEET_FONT_SIZE)

  def __init_props(self):
    self.padding = settings.RENDERER_PADDING
    self.profile_image_size = self.height - (self.padding + settings.RENDERER_HANDLE_FONT_SIZE)
    self.tweet_text_width = settings.RENDERER_TWEET_TEXT_WIDTH
    self.scroll_speed = settings.RENDERER_TEXT_SCROLL_SPEED
    self.back_colour = MAX_COLOUR
    self.fore_colour = 0
    self.__shared_buffer = self.__create_buffer()

  def __create_buffer(self, width = None, height = None, back_colour = None):
    if width is None:
      width = self.width
      
    if height is None:
      height = self.height

    if back_colour is None:
      back_colour = self.back_colour

    return ImageBuffer(width, height, back_colour)

  def __format_tweet_text(self, text):
    text = "      \n".join(textwrap.wrap(text, self.tweet_text_width))
    text += "      "
    return text

  def __render_text_to_width(self, text, font, width):
    (tw, th) = self.__get_text_size(text, font)
    text_buffer = self.__create_buffer(tw, th, self.fore_colour)
    text_buffer.draw.text((0, 0), "{0}   ".format(text), font = font, fill = self.back_colour)
    text_buffer.image = text_buffer.image.crop(text_buffer.image.getbbox())
    (tw, th) = text_buffer.image.size
    text_buffer_height = int(th * (self.width / tw))
    text_buffer.image = text_buffer.image.resize((self.width, text_buffer_height), resample = PIL.Image.BICUBIC)
    text_buffer.invert()
    return text_buffer.image

  def __get_text_size(self, text, font):
    return self.__shared_buffer.draw.textsize(text, font)

  def render_trend(self, trend):
    buffer = self.__create_buffer()
    trend_text = trend.name.upper()
    text_image = self.__render_text_to_width(trend_text, self.trend_font, self.width)
    (tw, th) = text_image.size
    tx = 0
    ty = int((self.height - th) / 2)
    buffer.image.paste(text_image, (tx, ty))
    return buffer.image

  def render_tweet_author(self, tweet):
    buffer = self.__create_buffer()
    profile_pic = tweet.profile_pic.resize((self.profile_image_size, self.profile_image_size), resample = PIL.Image.BICUBIC)
    ix = int((self.width - self.profile_image_size) / 2)
    buffer.image.paste(profile_pic, (ix, 0))

    handle = tweet.user
    (tw, th) = self.__get_text_size(handle, self.handle_font)
    tx = int((self.width - tw) / 2)
    ty = self.height - th
    buffer.draw.text((tx, ty), "{0}   ".format(handle), font = self.handle_font, fill = self.fore_colour)
    return buffer.image

  def render_tweet_text(self, tweet):
    text = self.__format_tweet_text(tweet.text)
    (tw, th) = self.__get_text_size(text, self.tweet_font)
    th += self.padding

    if th < self.height:
      buffer_height = self.height
    else:
      buffer_height = th
      
    buffer = self.__create_buffer(self.width, buffer_height)
    buffer.draw.text((0, 0), text, font = self.tweet_font, fill = self.fore_colour)

    has_more_pages = True
    y = 0
    while has_more_pages:
      if y + self.height > th:
        has_more_pages = False
        if th > self.height:
          y = th - self.height
      tweet_text_part = buffer.image.crop((0, y, self.width, y + self.height))
      y += self.height * self.scroll_speed
      yield tweet_text_part

  def render_tweet_images(self, tweet):
    for tweet_image in tweet.images:
      buffer = self.__create_buffer()
      (iw, ih) = tweet_image.size
      resized_ih = self.height
      resized_iw = int(iw * (resized_ih / ih))
      tweet_image = tweet_image.resize((resized_iw, resized_ih), resample = PIL.Image.BICUBIC)
      ix = int((self.width - resized_iw) / 2)
      iy = 0
      buffer.image.paste(tweet_image, (ix, iy))
      yield buffer.image



class ImageBuffer(object):
  def __init__(self, width, height, back_colour):
    self.width = width
    self.height = height
    self.image = Image.new(IMAGE_MODE, (self.width, self.height), back_colour)
    self.draw = ImageDraw.Draw(self.image)

  def resize(self, width, height):
    self.width = width
    self.height = height
    self.image = self.image.resize((width, height))

  def invert(self):
    pixels = self.image.load()
    (w, h) = self.image.size
    for x in range(0, w):
      for y in range(0, h):
        pixels[x, y] = MAX_COLOUR - pixels[x, y]