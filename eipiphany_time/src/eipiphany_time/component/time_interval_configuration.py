class TimeIntervalConfiguration(object):
  def __init__(self):
    self.__interval_seconds = 10

  @property
  def interval_seconds(self):
    return self.__interval_seconds

  @interval_seconds.setter
  def interval_seconds(self, value):
    self.set_interval_seconds(value)

  def set_interval_seconds(self, value):
    self.__interval_seconds = value
    return self
