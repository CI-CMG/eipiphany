from ....src.eipiphany_file.component.file_configuration import FileSourceConfiguration
from ....src.eipiphany_file.component.file_source import FileSource


class TestExchange(object):

  # def setup_method(self):
  #   self.teardown_method()
  #
  # def teardown_method(self):
  #   jdbc.query("DELETE FROM cruise.PEOPLE_AND_SOURCES")

  def test_simple(self):
    exchange = FileSource(FileSourceConfiguration().set_directory("foo"))

