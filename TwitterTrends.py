import TwitterApi, TwitterRenderer
import time, logging, settings

logging.basicConfig(level=logging.DEBUG)

api = TwitterApi.Api()
renderer = TwitterRenderer.Renderer()


while (True):

  try:

    trends = api.GetTrends()
    for trend in trends:
      tweets = api.GetTrendTweets(trend, settings.TWITTER_TWEET_COUNT)
      renderer.RenderTrend(trend)
      time.sleep(settings.FLOW_TREND_DISPLAY_TIME)
      for tweet in tweets:
        renderer.RenderTweetAuthor(tweet, settings.FLOW_AUTHOR_DISPLAY_TIME)
        renderer.RenderTweetText(tweet, settings.FLOW_TWEET_DISPLAY_TIME)
        renderer.RenderTweetImages(tweet, settings.FLOW_TWEET_IMAGE_DISPLAY_TIME)

  except IOError as e:
        logging.debug(e)
        
  except KeyboardInterrupt:    
      logging.debug("ctrl + c:")
      renderer.Shutdown()
      exit()