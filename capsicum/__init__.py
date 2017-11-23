# -*- coding:utf-8 -*-

import logging


class Habanero(object):
    def __init__(self):
        pass


# Set default logging handler to avoid "No handler found" warnings.


try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
print(__name__)
