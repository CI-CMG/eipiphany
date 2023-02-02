import abc

from ..internal.route import Route
from .default_error_handler import DefaultErrorHandler


class RouteBuilder(metaclass=abc.ABCMeta):

  def __init__(self, *args, **kw):
    super().__init__(*args, **kw)
    self._routes = []
    self.__default_error_handler = DefaultErrorHandler()

  def _from(self, eip_context, endpoint_id, route_id = None):
    route = Route(eip_context, endpoint_id, route_id if route_id else str(self))
    self._routes.append(route)
    return route

  def _error_handler(self, error_handler):
    self.__default_error_handler = error_handler

  @abc.abstractmethod
  def build(self, eip_context):
    pass

  def get_routes(self):
    return self._routes

  @property
  def error_handler(self):
    return self.__default_error_handler

