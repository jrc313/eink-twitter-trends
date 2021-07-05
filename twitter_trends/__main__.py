import argparse

parser = argparse.ArgumentParser(description = "Twitter Trends Viewer application")

parser.add_argument("-epaper", action = "store_true", dest = "epaper", default = False,
                    help = "Start application with epaper screen")
parser.add_argument("-test", action = "store_true", dest = "test", default = False,
                    help = "Start application with test screen")

args = parser.parse_args()

if args.epaper:
  from twitter_trends.epaper_app import epaper_app
  epaper_app()

elif args.test:
  from twitter_trends.test_app import test_app
  test_app()

else:
  from twitter_trends.test_app import test_app
  test_app()