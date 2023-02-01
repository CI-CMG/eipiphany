from datetime import datetime

from eipiphany_core.framework.base.eip_context import EipContext
from eipiphany_core.framework.base.endpoint import Endpoint
from eipiphany_core.framework.base.route_builder import RouteBuilder
from eipiphany_core.framework.test_support.eip_test_context import \
  EipTestContext

from ....src.eipiphany_time.component.time_interval_configuration import \
  TimeIntervalConfiguration
from ....src.eipiphany_time.component.time_interval_endpoint import \
  TimeIntervalEndpoint

class MyTestEndpoint(Endpoint):

  def __init__(self, primary_id):
    super().__init__(primary_id)

  def process(self, exchange, configuration):
    print("MyTestProcessor")
    print(exchange.body)

  def get_prefix(self):
    return 'my-test'

  def get_source(self):
    raise Exception("MyTestEndpoint only supports consumer endpoints")

class MyRouteBuilder(RouteBuilder):

  def build(self, eip_context):
    self._from(eip_context, 'time-interval:my-time').to(eip_context, 'my-test:the-end')

class TestTimeIntervalSource(object):

  def test_simple(self):


    with EipTestContext(EipContext()) as eip_context:

      eip_context.register_endpoint(MyTestEndpoint("the-end"))
      eip_context.register_endpoint(TimeIntervalEndpoint('my-time', TimeIntervalConfiguration().set_interval_seconds(1)))
      eip_context.add_route_builder(MyRouteBuilder())

      eip_context.mock_endpoint_and_skip('my-test:the-end', expected_message_count=2)

      eip_context.start()

      assert len(eip_context.get_endpoint('my-test:the-end').exchanges) == 2
      assert str(eip_context.get_endpoint('my-test:the-end').exchanges[0].body).startswith(str(datetime.now())[0:10])
      assert str(eip_context.get_endpoint('my-test:the-end').exchanges[1].body).startswith(str(datetime.now())[0:10])

