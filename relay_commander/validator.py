# -*- coding: utf-8 -*-
"""
relay_commander.validator
~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides helper functions that validate CLI input.
"""
import os
import sys

from relay_commander.util import LOG

_VALID_STATES = ['on', 'off']
"""Internal constant that defines a valid ``state`` argument."""
_REQUIRED_LD_API_VARS = ['LD_API_KEY']
_REQUIRED_REDIS_VARS = ['REDIS_HOSTS']
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
    if not os.getenv(envvar):  # test if env var is empty
        raise KeyError(
            "Required ENVVAR: {0} is empty".format(envvar))
    return True


def valid_state(state: str) -> bool:
    """Validate State Argument

    Checks that either 'on' or 'off' was entered as an argument to the
    CLI and make it lower case.

    :param state: state to validate.

    :returns: True if state is valid.

    .. versionchanged:: 0.0.12
        This moethod was renamed from validateState to valid_state to conform
        to PEP-8. Also removed "magic" text for state and instead reference the
        _VALID_STATES constant.
    """
    lower_case_state = state.lower()

    if lower_case_state in _VALID_STATES:
        return True
    return False


def valid_ld_api_vars() -> bool:
    """Validate that required env vars exist.

    :returns: True if required env vars exist.

    .. versionadded:: 0.0.12
    """
    for envvar in _REQUIRED_LD_API_VARS:
        try:
            _check_env_var(envvar)
        except KeyError as ex:
            LOG.error(ex)
            sys.exit(1)
    return True

def valid_redis_vars() -> bool:
    """Validate that required env vars exist.

    :returns: True if required env vars exist.

    .. versionadded:: 0.0.12
    """
    for envvar in _REQUIRED_REDIS_VARS:
        try:
            _check_env_var(envvar)
        except KeyError as ex:
            LOG.error(ex)
            sys.exit(1)
