from datetime import datetime

from eipiphany_core.framework.base.eip_context import EipContext
from eipiphany_core.framework.base.endpoint import Endpoint
from eipiphany_core.framework.base.route_builder import RouteBuilder
from eipiphany_core.framework.test_support.eip_test_context import \
  EipTestContext

from ....src.eipiphany_time.component.time_interval_source import TimeIntervalSource

class MyTestEndpoint(Endpoint):
  def __init__(self, *args, **kw):
    super().__init__(*args, **kw)

  def process(self, exchange, configuration):
    print("MyTestProcessor")
    print(exchange.body)

class MyRouteBuilder(RouteBuilder):
  def __init__(self, timer_source, *args, **kw):
    super().__init__(*args, **kw)
    self.__timer_source = timer_source

  def build(self, eip_context):
    self._from(self.__timer_source, route_id='timer').to(eip_context, 'the_end')

class TestTimeIntervalSource(object):

  def test_simple(self):


    with EipTestContext(EipContext()) as eip_context:

      eip_context.register_endpoint('the_end', MyTestEndpoint())
      eip_context.add_route_builder(MyRouteBuilder(TimeIntervalSource(1)))

      eip_context.mock_endpoint_and_skip('the_end', expected_message_count=2)

      eip_context.start()

      assert len(eip_context.get_endpoint('the_end').exchanges) == 2
      assert str(eip_context.get_endpoint('the_end').exchanges[0].body).startswith(str(datetime.now())[0:10])
      assert str(eip_context.get_endpoint('the_end').exchanges[1].body).startswith(str(datetime.now())[0:10])

