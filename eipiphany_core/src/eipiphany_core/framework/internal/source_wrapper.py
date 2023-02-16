import logging
from logging.handlers import QueueHandler


class SourceWrapper:

  def __init__(self, source, route, logging_queue):
    self._source = source
    self.__route = route
    self.__logging_queue = logging_queue

  def wait_for_events(self):
    root = logging.getLogger()
    root.addHandler(QueueHandler(self.__logging_queue))
    root.setLevel(logging.DEBUG)
    while True:
      exchange = self._source.wait_for_event()
      self.__route.run(exchange)

  def start(self):
    return self._source.start()