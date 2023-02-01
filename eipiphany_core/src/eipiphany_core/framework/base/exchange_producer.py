class ExchangeProducer(object):

  def __init__(self, context):
    self.__context = context

  def send(self, exchange, endpoint_id, configuration = None):
    self.__context.get_endpoint(endpoint_id).process(exchange, configuration)