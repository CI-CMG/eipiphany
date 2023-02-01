from ..base.endpoint import Endpoint

class MockEndpoint(Endpoint):
  def __init__(self, context, original_endpoint, expected_message_count):
    super().__init__()
    self.__exchanges = context.manager.list()
    self.__expected_message_count = expected_message_count
    self.__original_endpoint = original_endpoint

  def process(self, exchange, configuration):
    self.exchanges.append(exchange)
    if self.__original_endpoint:
      self.__original_endpoint.process(exchange, configuration)

  @property
  def exchanges(self):
    return self.__exchanges

  @property
  def expected_message_count(self):
    return self.__expected_message_count