"""
relay_commander.util
~~~~~~~~~~~~~~~~~~~~

General internal helper functions.
"""
import logging
import sys

log = logging.getLogger(sys.modules[__name__].__name__)
ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)
