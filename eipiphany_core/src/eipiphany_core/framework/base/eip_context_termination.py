import abc


class EipContextTermination(metaclass=abc.ABCMeta):

  @abc.abstractmethod
  def is_terminate(self, context):
    pass