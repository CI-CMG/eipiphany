import logging

from .error_handler import ErrorHandler

logger = logging.getLogger(__name__)


class DefaultErrorHandler(ErrorHandler):

  def handle_exception(self, exchange):
    logger.error("Exception in route (" + exchange.get_header(ErrorHandler.EXCEPTION_CAUGHT) + ") " + exchange.get_header(ErrorHandler.EXCEPTION_CAUGHT_DETAIL))
