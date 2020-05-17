import PIL
from PIL import Image, ImageDraw, ImageFont
import textwrap, html, sys, os, requests, io, logging, time

libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V2

import settings

class Renderer(object):

  def __init__(self):
    self.__InitDisplay()
    self.__LoadFonts()
    self.__InitBuffer()
    self.__InitProps()
  
  def __InitDisplay(self):
    self.epd = epd2in13_V2.EPD()
    self.__ClearDisplay()
    self.screen_width = self.epd.height
    self.screen_height = self.epd.width

  def __LoadFonts(self):
    self.trend_font = ImageFont.truetype(
      os.path.join(settings.RENDERER_ASSET_PATH, settings.RENDERER_TREND_FONT_NAME),
      settings.RENDERER_TREND_FONT_SIZE)
    self.handle_font = ImageFont.truetype(
      os.path.join(settings.RENDERER_ASSET_PATH, settings.RENDERER_HANDLE_FONT_NAME),
      settings.RENDERER_HANDLE_FONT_SIZE)
    self.tweet_font = ImageFont.truetype(
      os.path.join(settings.RENDERER_ASSET_PATH, settings.RENDERER_TWEET_FONT_NAME),
      settings.RENDERER_TWEET_FONT_SIZE)

  def __InitBuffer(self):
    self.buffer = Image.new("1", (self.screen_width, self.screen_height), 255)
    self.draw = ImageDraw.Draw(self.buffer)

  def __InitProps(self):
    self.padding = settings.RENDERER_PADDING
    self.profile_image_size = self.screen_height - (self.padding + settings.RENDERER_HANDLE_FONT_SIZE)
    self.tweet_text_width = settings.RENDERER_TWEET_TEXT_WIDTH

  def __ClearBuffer(self):
    self.draw.rectangle((0, 0, self.screen_width, self.screen_height), fill = 255)

  def __RenderBuffer(self):
    self.epd.displayPartial(self.epd.getbuffer(self.buffer))

  def __ClearDisplay(self):
    self.epd.init(self.epd.FULL_UPDATE)
    self.epd.Clear(0xFF)

  def __InitPartialUpdate(self):
    self.epd.displayPartBaseImage(self.epd.getbuffer(self.buffer))
    self.epd.init(self.epd.PART_UPDATE)

  def __FormatTweetText(self, text):
    text = "      \n".join(textwrap.wrap(text, self.tweet_text_width))
    text += "      "
    return text

  def __InvertImage(self, image):
    pixels = image.load()
    (w, h) = image.size
    for x in range(0, w):
      for y in range(0, h):
        pixels[x, y] = 255 - pixels[x, y]

  def __RenderTextToWidth(self, text, font, width):
    (tw, th) = self.draw.textsize(text, font)
    text_image = Image.new("1", (tw, th), 0)
    text_draw = ImageDraw.Draw(text_image)
    text_draw.text((0, 0), "{0}   ".format(text), font = font, fill = 255)
    text_image = text_image.crop(text_image.getbbox())
    (tw, th) = text_image.size
    text_image_height = int(th * (width / tw))
    text_image = text_image.resize((width, text_image_height), resample = PIL.Image.BICUBIC)
    self.__InvertImage(text_image)
    return text_image

  def RenderTrend(self, trend):
    self.__ClearBuffer()
    self.__ClearDisplay()
    self.__InitPartialUpdate()
    trend_text = trend.name.upper()
    text_image = self.__RenderTextToWidth(trend_text, self.trend_font, self.screen_width)
    (tw, th) = text_image.size
    tx = 0
    ty = int((self.screen_height - th) / 2)
    self.buffer.paste(text_image, (tx, ty))
    self.__RenderBuffer()

  def RenderTweetAuthor(self, tweet, delay):
    self.__ClearBuffer()
    profile_pic = tweet.profile_pic.resize((self.profile_image_size, self.profile_image_size), resample = PIL.Image.BICUBIC)
    ix = int((self.screen_width - self.profile_image_size) / 2)
    self.buffer.paste(profile_pic, (ix, 0))

    handle = tweet.user
    (tw, th) = self.draw.textsize(handle, self.handle_font)
    tx = int((self.screen_width - tw) / 2)
    ty = self.screen_height - th
    self.draw.text((tx, ty), "{0}   ".format(handle), font = self.handle_font, fill = 0)
    self.__RenderBuffer()
    time.sleep(delay)

  def RenderTweetText(self, tweet, delay):
    self.__ClearBuffer()
    text = self.__FormatTweetText(tweet.text)
    (tw, th) = self.draw.textsize(text, self.tweet_font)
    self.draw.text((0, 0), text, font = self.tweet_font, fill = 0)
    self.__RenderBuffer()
    time.sleep(delay)
    if th > self.screen_height:
      self.__ClearBuffer()
      ty = self.screen_height - (th + settings.RENDERER_PADDING)
      self.draw.text((0, ty), text, font = self.tweet_font, fill = 0)
      self.__RenderBuffer()
      time.sleep(delay)

  def RenderTweetImages(self, tweet, delay):
    for image in tweet.images:
      self.__ClearBuffer()
      (iw, ih) = image.size
      resized_ih = self.screen_height
      resized_iw = int(iw * (resized_ih / ih))
      image = image.resize((resized_iw, resized_ih), resample = PIL.Image.BICUBIC)
      ix = int((self.screen_width - resized_iw) / 2)
      iy = 0
      logging.debug("Drawing image of size ({0}, {1}) to ({2}, {3})".format(resized_iw, resized_ih, ix, iy))
      self.buffer.paste(image, (ix, iy))
      self.__RenderBuffer()
      time.sleep(delay)

  def Shutdown(self):
    self.__ClearDisplay()
    epd2in13_V2.epdconfig.module_exit()

    