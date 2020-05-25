import logging

from twitter_trends.core.director import Director
from twitter_trends.core.api.trends_api import TrendsApi
from twitter_trends.core.renderer import ImageRenderer
from twitter_trends.screens.epaper_screen import EPaperScreen

logging.basicConfig(level=logging.WARN)

def epaper_app():
  screen = EPaperScreen()
  trendsApi = TrendsApi()
  renderer = ImageRenderer(screen.width, screen.height)
  director = Director(screen, trendsApi, renderer)

  while (True):

    try:
      director.run()

    except IOError as e:
          logging.debug(e)
          
    except KeyboardInterrupt:    
        logging.debug("ctrl + c:")
        exit()