import abc

class Endpoint(metaclass=abc.ABCMeta):

  @abc.abstractmethod
  def process(self, exchange, configuration):
    pass
