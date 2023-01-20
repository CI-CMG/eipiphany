import abc

from ...framework.internal.route import Route
from ...component.error_handler.default_error_handler import DefaultErrorHandler


class RouteBuilder(metaclass=abc.ABCMeta):

  def __init__(self):
    self.__routes = []
    self.__error_handler = DefaultErrorHandler()

  def comes_from(self, source):
    route = Route(source, self.__error_handler)
    self.__routes.append(route)
    return route

  def error_handler(self, error_handler):
    self.__error_handler = error_handler

  @abc.abstractmethod
  def build(self):
    pass

  def get_routes(self):
    return self.__routes

  def start(self):
    joiners = []
    for route in self.__routes:
      joiners.append(route.start())
    return joiners

