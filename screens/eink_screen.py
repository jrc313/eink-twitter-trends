from waveshare_epd import epd2in13_V2

class EInkScreen(object):

  def __init__(self):
    self.epd = epd2in13_V2.EPD()
    self.clear()
    self.width = self.epd.height
    self.height = self.epd.width
    self.is_clear_frame = True

  def clear(self):
    self.epd.init(self.epd.FULL_UPDATE)
    self.epd.Clear(0xFF)
    self.is_clear_frame = True

  def render_frame(self, image):
    if (self.is_clear_frame):
      self.__init_partial_update(image)
    self.epd.displayPartial(self.epd.getbuffer(image))

  def __init_partial_update(self, image):
    self.epd.displayPartBaseImage(self.epd.getbuffer(image))
    self.epd.init(self.epd.PART_UPDATE)
    self.is_clear_frame = False

  def __del__(self):
    self.clear()
    epd2in13_V2.epdconfig.module_exit()