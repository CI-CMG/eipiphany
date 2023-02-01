import time

from ..base.default_eip_context_termination import DefaultEipContextTermination


class TestEipContextTermination(DefaultEipContextTermination):
  def __init__(self, timeout=20000):
    self.__timeout = timeout
    self.__mock_endpoints = []

  @property
  def mock_endpoints(self):
    return self.__mock_endpoints

  @mock_endpoints.setter
  def mock_endpoints(self, value):
    self.__mock_endpoints = value

  def is_terminate(self, context):
    term = super().is_terminate(context)
    if term:
      return True
    if self.__mock_endpoints:
      completed = 0
      for ep in self.__mock_endpoints:
        if len(ep.exchanges) >= ep.expected_message_count:
          completed += 1
      if completed == len(self.__mock_endpoints):
        return True
    current_time = round(time.time() * 1000)
    return current_time - context.start_time >= self.__timeout
