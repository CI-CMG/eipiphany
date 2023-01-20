from ....src.eipiphany_seda.component.queue_endpoint import QueueEndpoint


class TestExchange(object):

  # def setup_method(self):
  #   self.teardown_method()
  #
  # def teardown_method(self):
  #   jdbc.query("DELETE FROM cruise.PEOPLE_AND_SOURCES")

  def test_simple(self):
    exchange = QueueEndpoint(None)
