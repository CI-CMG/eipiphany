from ....src.eipiphany_seda.component.seda_endpoint import SedaEndpoint


class TestExchange(object):

  # def setup_method(self):
  #   self.teardown_method()
  #
  # def teardown_method(self):
  #   jdbc.query("DELETE FROM cruise.PEOPLE_AND_SOURCES")

  def test_simple(self):
    exchange = SedaEndpoint(None)
