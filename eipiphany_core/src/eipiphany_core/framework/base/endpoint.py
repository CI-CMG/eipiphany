import abc

class Endpoint(metaclass=abc.ABCMeta):

  def __init__(self, primary_id):
    self._primary_id = primary_id

  @abc.abstractmethod
  def get_prefix(self):
    pass

  @property
  def primary_id(self):
    return self._primary_id

  @abc.abstractmethod
  def process(self, exchange, configuration):
    pass

  @abc.abstractmethod
  def get_source(self):
    pass
