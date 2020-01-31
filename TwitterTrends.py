import TwitterApi
import TwitterRenderer
import time
import logging

logging.basicConfig(level=logging.DEBUG)

api = TwitterApi.Api()
renderer = TwitterRenderer.Renderer()


while (True):

  try:

    trends = api.GetTrends()
    for trend in trends:
      renderer.RenderTrend(trend)
      time.sleep(1)
      tweets = api.GetTrendTweets(trend)
      for tweet in tweets:
        renderer.RenderTweet(tweet, api.GetProfilePicture(tweet, False))
        time.sleep(3)

  except IOError as e:
        logging.debug(e)
        
  except KeyboardInterrupt:    
      logging.debug("ctrl + c:")
      renderer.Shutdown()
      exit()