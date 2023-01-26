from datetime import datetime

from eipiphany_core.framework.base.eipiphany_context import EipiphanyContext
from eipiphany_core.framework.base.processor import Processor
from eipiphany_core.framework.base.route_builder import RouteBuilder
from eipiphany_core.framework.test_support.eipiphany_test_context import \
  EipiphanyTestContext

from ....src.eipiphany_time.component.time_interval_source import TimeIntervalSource

class MyTestProcessor(Processor):
  def __init__(self, *args, **kw):
    super().__init__(*args, **kw)

  def process(self, exchange):
    print("MyTestProcessor")
    print(exchange.body)

class MyRouteBuilder(RouteBuilder):
  def __init__(self, timer_source, processor, *args, **kw):
    super().__init__(*args, **kw)
    self.__timer_source = timer_source
    self.__processor = processor

  def build(self):
    self._from(self.__timer_source, route_id='timer').to(self.__processor)



class TestTimeIntervalSource(object):

  def test_simple(self):

    with EipiphanyTestContext(EipiphanyContext()) as eip_context:
      source = TimeIntervalSource(1)
      processor = MyTestProcessor()
      eip_context.add_route_builder(MyRouteBuilder(source, processor))
      eip_context.mock_endpoint_and_skip('timer', processor, expected_message_count=2)
      eip_context.start()

      assert len(eip_context.mock_endpoints[processor].exchanges) == 2
      assert str(eip_context.mock_endpoints[processor].exchanges[0].body).startswith(str(datetime.now())[0:10])
      assert str(eip_context.mock_endpoints[processor].exchanges[1].body).startswith(str(datetime.now())[0:10])

