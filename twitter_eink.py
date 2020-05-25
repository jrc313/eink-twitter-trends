import logging

from director import Director
from twitter_trends.trends_api import TrendsApi
from twitter_trends.renderer import ImageRenderer
from screens.eink_screen import EInkScreen

logging.basicConfig(level=logging.WARN)

screen = EInkScreen()
trendsApi = TrendsApi()
renderer = ImageRenderer(screen.width, screen.height)
director = Director(screen, trendsApi, renderer)

while (True):

  try:

    director.Run()

  except IOError as e:
        logging.debug(e)
        
  except KeyboardInterrupt:    
      logging.debug("ctrl + c:")
      exit()