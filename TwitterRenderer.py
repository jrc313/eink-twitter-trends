import PIL
from PIL import Image, ImageDraw, ImageFont
import textwrap
import html

import sys
import os

import requests
import io

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
    self.profile_image_size = settings.RENDERER_PROFILE_IMAGE_SIZE
    self.profile_image_x = self.padding
    self.profile_image_y = self.padding

    self.text_x = self.profile_image_size + (self.padding * 2)
    self.text_y = self.padding

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

  

  def __FormatTweetText(self, tweet):
    text = tweet.text
    for url in tweet.urls:
        text = text.replace(url.url, "")
    text = text.replace(u"\n", u" ")
    text = text.replace(u"\r", u"")
    text = html.unescape(text)
    text = " \n".join(textwrap.wrap(text, 30))
    text += " "
    return text

  def RenderTrend(self, trend):
    self.__ClearBuffer()
    self.__InitPartialUpdate()
    trend_text = trend.name.upper()
    (twidth, theight) = self.draw.textsize(trend_text, self.trend_font)
    tx = int((self.screen_width - twidth) / 2)
    ty = int((self.screen_height - theight) / 2)
    self.draw.text((tx, ty), trend_text, font = self.trend_font, fill = 0)
    self.__RenderBuffer()

  def RenderTweet(self, tweet, profile_pic):
    self.__ClearBuffer()
    self.buffer.paste(profile_pic, (self.profile_image_x, self.profile_image_y))
    text = u"@{0}\n{1}".format(tweet.user.screen_name, self.__FormatTweetText(tweet))
    self.draw.text((self.text_x, self.text_y), text, font = self.tweet_font, fill = 0)
    self.__RenderBuffer()

  def Shutdown(self):
    self.__ClearDisplay()
    epd2in13_V2.epdconfig.module_exit()

    