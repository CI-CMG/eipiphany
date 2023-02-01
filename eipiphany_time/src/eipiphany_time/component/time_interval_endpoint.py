from eipiphany_core.framework.base.endpoint import Endpoint

from .time_interval_configuration import TimeIntervalConfiguration
from .time_interval_source import TimeIntervalSource


class TimeIntervalEndpoint(Endpoint):

  def __init__(self, primary_id, source_configuration = None):
    super().__init__(primary_id)
    self.__default_config = TimeIntervalConfiguration()
    self.__source_configuration = source_configuration
    if not self.__source_configuration:
      self.__source_configuration = self.__default_config
    self.__source = TimeIntervalSource(self.__source_configuration)

  def get_prefix(self):
    return 'time-interval'

  def process(self, exchange, configuration):
    raise Exception("time-interval endpoint only supports producer endpoints")

  def get_source(self):
    return self.__source