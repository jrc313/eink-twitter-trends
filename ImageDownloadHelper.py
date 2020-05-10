import io, requests, logging
from PIL import Image


def Download(url):
  logging.debug("Downloading image: {0}".format(url))
  image_stream = requests.get(url, stream = True)
  if image_stream.status_code == 200:
    logging.debug("Download success")
    return Image.open(io.BytesIO(image_stream.content))
  return None