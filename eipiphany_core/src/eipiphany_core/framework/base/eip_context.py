import time
from multiprocessing import Manager

from .default_eip_context_termination import DefaultEipContextTermination
from .exchange_producer import ExchangeProducer


class EipContext(object):
  def __init__(self, termination=DefaultEipContextTermination()):
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
      process.terminate()
      process.join()
      process.close()

  def start(self):
    for route_builder in self.__route_builders:
      route_builder.build(self)
      for route in route_builder.get_routes():
        self._routes.append(route)
    self.__start_time = round(time.time() * 1000)
    for route in self._routes:
      for process in route.start():
        self.__processes.append(process)
    terminate = False
    while not terminate:
      time.sleep(1)
      terminate = self._termination.is_terminate(self)
    self.__terminate()

  @property
  def manager(self):
    return self.__manager

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
