import logging
import logging.config
import time
from importlib import reload
from logging.handlers import QueueHandler
from multiprocessing import Manager, Queue, Process

from .default_eip_context_termination import DefaultEipContextTermination
from .exchange_producer import ExchangeProducer
from ..internal.process_wrapper import ProcessWrapper

def _logging_process(queue, logging_config):
  logging.shutdown()
  reload(logging)
  logging.config.dictConfig(logging_config)
  while True:
    record = queue.get()
    if record is None:
      break
    logger = logging.getLogger(record.name)
    logger.handle(record)


_DEFAULT_LOGGING_CONFIG = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'simple': {
      'format': '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
      'datefmt': '%Y-%m-%d %H:%M:%S'
    }
  },
  'handlers': {
    'console': {
      'class': 'logging.StreamHandler',
      'formatter': 'simple',
      'stream': 'ext://sys.stdout'
    }
  },
  'loggers': {
    'eipiphany': {
      'level': 'INFO',
      'handlers': ['console'],
      'propagate': False
    },
  },
  'root': {
    'level': 'INFO',
    'handlers': ['console']
  }
}

_NAME_TO_LEVEL = {
  'CRITICAL': logging.CRITICAL,
  'FATAL': logging.FATAL,
  'ERROR': logging.ERROR,
  'WARN': logging.WARNING,
  'WARNING': logging.WARNING,
  'INFO': logging.INFO,
  'DEBUG': logging.DEBUG,
  'NOTSET': logging.NOTSET,
}

def _get_min_logging_level(logging_config):
  min_level = None
  loggers = logging_config.get('loggers')
  root = logging_config.get('root')
  if root and root.get('level'):
    level = _NAME_TO_LEVEL[root.get('level')]
    if min_level is None or level < min_level:
      min_level = level
  if loggers:
    for logger_name in loggers:
      logger = loggers[logger_name]
      if logger.get('level'):
        level = _NAME_TO_LEVEL[logger.get('level')]
        if min_level is None or level < min_level:
          min_level = level
  if min_level is None:
    min_level = logging.DEBUG
  return min_level



class EipContext(object):
  def __init__(self, termination=DefaultEipContextTermination(), logging_config=_DEFAULT_LOGGING_CONFIG):
    self.__logging_queue = Queue()
    self.__min_logging_level = _get_min_logging_level(logging_config)
    logging.shutdown()
    reload(logging)
    root = logging.getLogger()
    root.addHandler(QueueHandler(self.__logging_queue))
    root.setLevel(self.__min_logging_level)
    self.__logging_listener = Process(target=_logging_process, args=(self.__logging_queue, logging_config))
    self.__logging_listener.daemon = True
    self.__logging_listener.start()
    self.__manager = Manager()
    self._routes = []
    self.__processes = []
    self.__start_time = None
    self._termination = termination
    self.__endpoint_registry = {}
    self.__route_builders = []
    self.__exchange_producer = ExchangeProducer(self)

  def get_exchange_producer(self):
    return self.__exchange_producer

  def get_endpoint(self, endpoint_id):
    return self.__endpoint_registry[endpoint_id]

  def register_endpoint(self, endpoint):
    self._register_endpoint_internal(endpoint, False)

  def _register_endpoint_internal(self, endpoint, allow_override):
    prefix = endpoint.get_prefix()
    epid = prefix + ":" + endpoint.primary_id
    if not allow_override and self.__endpoint_registry.get(epid):
      raise Exception(epid + " is already registered")
    self.__endpoint_registry[epid] = endpoint

  def add_route_builder(self, route_builder):
    self.__route_builders.append(route_builder)
    return self

  def __terminate(self):
    for process in self.__processes:
      process.process.terminate()
      process.process.join()
      process.process.close()

  def start(self):
    self._start_internal(None)

  def _start_internal(self, after_start):
    for route_builder in self.__route_builders:
      route_builder.build(self)
      for route in route_builder.get_routes():
        route._set_default_error_handler(route_builder.error_handler)
        self._routes.append(route)
    self.__start_time = round(time.time() * 1000)
    for route in self._routes:
      for process in route.start():
        self.__processes.append(ProcessWrapper(process))
    if after_start:
      after_start.daemon = True
      after_start.start()
      self.__processes.append(ProcessWrapper(after_start, can_terminate=True))
    terminate = False
    while not terminate:
      time.sleep(1)
      terminate = self._termination.is_terminate(self)
    self.__terminate()

  @property
  def manager(self):
    return self.__manager

  @property
  def logging_queue(self):
    return self.__logging_queue

  @property
  def min_logging_level(self):
    return self.__min_logging_level

  @property
  def processes(self):
    return self.__processes

  @property
  def start_time(self):
    return self.__start_time

  def __enter__(self):
    self.__manager.__enter__()
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.__manager.__exit__(exc_type, exc_val, exc_tb)
