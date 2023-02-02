from .eip_context_termination import EipContextTermination


class DefaultEipContextTermination(EipContextTermination):
  def is_terminate(self, context):
    if not len(context.processes):
      return True
    for process in context.processes:
      if not process.can_terminate and not process.process.is_alive():
        return True
    return False
