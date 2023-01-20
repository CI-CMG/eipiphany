import logging

from .exchange_handler import ExchangeHandler
from ...framework.base.error_handler import ErrorHandler
from .source_wrapper import SourceWrapper

logger = logging.getLogger(__name__)



class Route(object):

  def __init__(self, source, error_handler):
    self.__source = source
    self.__source_wrapper = SourceWrapper(source, self)
    source.set_source_wrapper(self.__source_wrapper)
    self.__exchange_handlers = []
    self.__error_handler = error_handler

  # todo move this to separate class
  def process(self, exchange):
    try:
      for exchange_handler in self.__exchange_handlers:
        if exchange_handler.processor:
          exchange_handler.processor.process(exchange)
        elif exchange_handler.filter:
          keep_going = exchange_handler.filter.filter(exchange)
          if not keep_going:
            break
        else:
          raise Exception("Internal error: invalid exchange handler")
      self.__source.event_success(exchange)
    except Exception as err:
      try:
        exchange.set_header(ErrorHandler.EXCEPTION_CAUGHT, err)
        self.__source.event_failure(err, exchange)
        self.__error_handler.handle_exception(exchange)
      except Exception as err2:
        logger.error("Exception in error handler", exc_info=err2)
        logger.error("Original exception", exc_info=err)

  def to(self, processor):
    self.__exchange_handlers.append(ExchangeHandler().set_processor(processor))
    return self

  def filter(self, filter):
    self.__exchange_handlers.append(ExchangeHandler().set_filter(filter))
    return self

  def error_handler(self, error_handler):
    self.__error_handler = error_handler
    return self

  def start(self):
    return self.__source_wrapper.start()

