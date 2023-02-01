from multiprocessing import JoinableQueue

from eipiphany_core.framework.base.endpoint import Endpoint

from .seda_configuration import SedaConfiguration
from .seda_source import SedaSource


class SedaEndpoint(Endpoint):

  def __init__(self, primary_id, source_configuration = None):
    super().__init__(primary_id)
    self.__default_config = SedaConfiguration()
    self.__source_configuration = source_configuration
    if not self.__source_configuration:
      self.__source_configuration = self.__default_config
    self.__queue = JoinableQueue(maxsize=self.__source_configuration.max_size)
    self.__source = SedaSource(self.__queue, self.__source_configuration)

  def get_prefix(self):
    return 'seda'

  def process(self, exchange, configuration):
    config = configuration
    if not config:
      config = self.__default_config
    self.__queue.put(exchange, config.block_when_full)

  def get_source(self):
    return self.__source