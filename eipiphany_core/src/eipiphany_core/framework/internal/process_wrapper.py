class ProcessWrapper(object):
  def __init__(self, process, can_terminate = False):
    self.__process = process
    self.__can_terminate = can_terminate

  @property
  def process(self):
    return self.__process

  @property
  def can_terminate(self):
    return self.__can_terminate