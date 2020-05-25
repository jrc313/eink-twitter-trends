import logging, io

from twitter_trends.core.director import Director
from twitter_trends.core.api.offline_trends_api import OfflineTrendsApi
from twitter_trends.core.renderer import ImageRenderer
from twitter_trends.screens.test_screen import TestScreen

logging.basicConfig(level=logging.DEBUG)

def test_app():
  screen = TestScreen()
  trendsApi = OfflineTrendsApi("twitter_trends/resources/trends-short.yaml")
  renderer = ImageRenderer(screen.width, screen.height)
  director = Director(screen, trendsApi, renderer)
  
  while (True):

    try:
      director.run()
    
    except KeyboardInterrupt:    
        logging.debug("ctrl + c:")
        exit()