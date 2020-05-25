import logging, io

from director import Director
from twitter_trends.offline_trends_api import OfflineTrendsApi
from twitter_trends.renderer import ImageRenderer
from screens.test_screen import TestScreen

logging.basicConfig(level=logging.DEBUG)

screen = TestScreen()
trendsApi = OfflineTrendsApi("trends-short.yaml")
renderer = ImageRenderer(screen.width, screen.height)
director = Director(screen, trendsApi, renderer)


while (True):

  try:
    director.run()
  
  except KeyboardInterrupt:    
      logging.debug("ctrl + c:")
      exit()