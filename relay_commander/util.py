"""
relay_commander.util
~~~~~~~~~~~~~~~~~~~~

General internal helper functions.

.. versionadded:: 0.0.12
"""
import logging
import sys

# Configure Logging
LOG = logging.getLogger(sys.modules[__name__].__name__)
_CH = logging.StreamHandler(sys.stdout)
_FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s')
_CH.setFormatter(_FORMATTER)
LOG.addHandler(_CH)
