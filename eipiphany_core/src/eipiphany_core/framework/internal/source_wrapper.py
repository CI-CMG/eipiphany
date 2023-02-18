import logging
from importlib import reload
from logging.handlers import QueueHandler


class SourceWrapper:

  def __init__(self, source, route, logging_queue, logging_level):
    self._source = source
    self.__route = route
    self.__logging_queue = logging_queue
    self.__logging_level = logging_level

  def wait_for_events(self):
    logging.shutdown()
    reload(logging)
    root = logging.getLogger()
    root.addHandler(QueueHandler(self.__logging_queue))
    root.setLevel(self.__logging_level)
    while True:
      exchange = self._source.wait_for_event()
      self.__route.run(exchange)

  def start(self):
    return self._source.start()