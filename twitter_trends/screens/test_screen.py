from PIL import Image
import io, logging, os

class TestScreen(object):

  def __init__(self):
    self.width = 250
    self.height = 122
    self.clear_buffer = Image.new("1", (self.width, self.height), 255)

  def clear(self):
    self.render_frame(self.clear_buffer)

  def render_frame(self, image):
    logging.debug("Rendering frame")
    image.save("./testimage.png", "PNG")

