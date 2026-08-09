import logging


class RouteLogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return record.getMessage().find("/health") == -1
