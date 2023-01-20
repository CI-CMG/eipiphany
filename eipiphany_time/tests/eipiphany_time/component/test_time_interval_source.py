from ....src.eipiphany_time.component.time_interval_source import TimeIntervalSource


class TestTimeIntervalSource(object):

  # def setup_method(self):
  #   self.teardown_method()
  #
  # def teardown_method(self):
  #   jdbc.query("DELETE FROM cruise.PEOPLE_AND_SOURCES")

  def test_simple(self):
    exchange = TimeIntervalSource(None)