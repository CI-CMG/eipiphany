class SedaConfiguration(object):
  def __init__(self):
    self.__max_size = 1000
    self.__block_when_full = True
    self.__concurrent_consumers = 1


  @property
  def max_size(self):
    return self.__max_size

  @max_size.setter
  def max_size(self, value):
    self.set_max_size(value)

  def set_max_size(self, value):
    self.__max_size = value
    return self

  @property
  def block_when_full(self):
    return self.__block_when_full

  @block_when_full.setter
  def block_when_full(self, value):
    self.set_block_when_full(value)

  def set_block_when_full(self, value):
    self.__block_when_full = value
    return self

  @property
  def concurrent_consumers(self):
    return self.__concurrent_consumers

  @concurrent_consumers.setter
  def concurrent_consumers(self, value):
    self.set_concurrent_consumers(value)

  def set_concurrent_consumers(self, value):
    self.__concurrent_consumers = value
    return self
