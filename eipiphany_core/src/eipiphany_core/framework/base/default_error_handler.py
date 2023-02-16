import logging

from .error_handler import ErrorHandler

logger = logging.getLogger('eipiphany.core.framework.base.DefaultErrorHandler')


class DefaultErrorHandler(ErrorHandler):

  def handle_exception(self, exchange):
    logger.error("Exception in route (" + exchange.get_header(ErrorHandler.EXCEPTION_CAUGHT) + ") " + exchange.get_header(ErrorHandler.EXCEPTION_CAUGHT_DETAIL))
    # print("Exception in route (" + exchange.get_header(ErrorHandler.EXCEPTION_CAUGHT) + ") " + exchange.get_header(ErrorHandler.EXCEPTION_CAUGHT_DETAIL))
