from eipiphany_core.framework.base.endpoint import Endpoint

from .file_configuration import FileConfiguration
from .file_source import FileSource


class FileEndpoint(Endpoint):

  def __init__(self, primary_id, source_configuration = None):
    super().__init__(primary_id)
    self.__default_config = FileConfiguration()
    self.__source_configuration = source_configuration
    if not self.__source_configuration:
      self.__source_configuration = self.__default_config
    self.__source = FileSource(self.__source_configuration)

  def get_prefix(self):
    return 'file'

  def process(self, exchange, configuration):
    raise Exception("Not implemented yet")

  def get_source(self):
    return self.__source