from ..base.endpoint import Endpoint

class MockEndpoint(Endpoint):
  def __init__(self, context, original_endpoint, skip, expected_message_count):
    super().__init__(original_endpoint.primary_id)
    self.__exchanges = context.manager.list()
    self.__expected_message_count = expected_message_count
    self.__original_endpoint = original_endpoint
    self.__skip = skip

  def get_prefix(self):
    return self.__original_endpoint.get_prefix()

  def process(self, exchange, configuration):
    self.exchanges.append(exchange)
    if not self.__skip:
      self.__original_endpoint.process(exchange, configuration)

  def get_source(self):
    return self.__original_endpoint.get_source()

  @property
  def exchanges(self):
    return self.__exchanges

  @property
  def expected_message_count(self):
    return self.__expected_message_count