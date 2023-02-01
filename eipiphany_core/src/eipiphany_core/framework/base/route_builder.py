import abc

from ...framework.internal.route import Route
from ...component.error_handler.default_error_handler import DefaultErrorHandler


class RouteBuilder(metaclass=abc.ABCMeta):

  def __init__(self, *args, **kw):
    super().__init__(*args, **kw)
    self._routes = []
    self._error_handler = DefaultErrorHandler()

  def _from(self, eip_context, endpoint_id, route_id = None):
    route = Route(eip_context, endpoint_id, self._error_handler, route_id if route_id else str(self))
    self._routes.append(route)
    return route

  def _error_handler(self, error_handler):
    self._error_handler = error_handler

  @abc.abstractmethod
  def build(self, eip_context):
    pass

  def get_routes(self):
    return self._routes

