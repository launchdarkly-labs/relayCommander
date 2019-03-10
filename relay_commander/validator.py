# -*- coding: utf-8 -*-
"""
relay_commander.validator
~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides helper functions that validate CLI input.

.. autodata:: _VALID_STATES
.. autodata:: _REQUIRED_ENV_VARS

.. versionchanged:: 0.0.12

    * Added valid_env_vars() function
    * Added internal constants for valid state and required env vars.
"""
import os
import sys
import logging

logger = logging.getLogger(__name__)

_VALID_STATES: list = ['on', 'off']
"""Internal constant that defines a valid ``state`` argument."""
_REQUIRED_ENV_VARS: list = ['LD_API_KEY', 'REDIS_HOSTS']
"""Internal constant that defines required environment variables."""


def _check_env_var(envvar: str) -> bool:
    """Check Environment Variable to verify that it is set and not empty.

    :param envvar: Environment Variable to Check.

    :returns: True if Environment Variable is set and not empty.

    :raises: KeyError if Environment Variable is not set or is empty.

    .. versionadded:: 0.0.12
    """
    if os.getenv(envvar) is None:
        raise KeyError(
            "Required ENVVAR: {0} is not set".format(envvar))
    if len(os.getenv(envvar)) < 1:
        raise KeyError(
            "Required ENVVAR: {0} is empty".format(envvar))
    else:
        return True


def valid_state(state: str) -> bool:
    """Validate State Argument

    Checks that either 'on' or 'off' was entered as an argument to the
    CLI and make it lower case.

    :param state: state to validate.

    :returns: True if state is valid.

    .. versionchanged:: 0.0.12
    Refactor for pep8, renamed from validateState to valid_state. Also removed
    "magic" text for state and now define as constant _VALID_STATES.
    """
    lower_case_state = state.lower()

    if lower_case_state in _VALID_STATES:
        return True
    return False


def valid_env_vars() -> bool:
    """Validate that required env vars exist.

    :returns: True if required env vars exist.

    .. versionadded:: 0.0.12
    """
    for e in _REQUIRED_ENV_VARS:
        try:
            _check_env_var(e)
        except KeyError as ex:
            logger.error(ex)
            sys.exit(1)

    return True
