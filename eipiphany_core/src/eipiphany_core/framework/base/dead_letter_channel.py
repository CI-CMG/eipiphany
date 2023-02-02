from .error_handler import ErrorHandler


class DeadLetterChannel(ErrorHandler):

  def __init__(self, eip_context, endpoint_id, endpoint_configuration = None):
    self.__endpoint = eip_context.get_endpoint(endpoint_id)
    self.__endpoint_configuration = endpoint_configuration
    self.__prep_processor = None

  def on_prepare_failure(self, processor):
    self.__prep_processor = processor
    return self

  def handle_exception(self, exchange):
    if self.__prep_processor:
      self.__prep_processor.process(exchange)
    self.__endpoint.process(exchange, self.__endpoint_configuration)




