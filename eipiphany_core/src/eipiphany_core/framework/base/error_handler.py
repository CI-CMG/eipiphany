import abc

class ErrorHandler(metaclass=abc.ABCMeta):

  EXCEPTION_CAUGHT = 'ExceptionCaught'
  EXCEPTION_CAUGHT_DETAIL = 'ExceptionCaughtDetail'

  @abc.abstractmethod
  def handle_exception(self, exchange):
    pass

