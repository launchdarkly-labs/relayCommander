# -*- coding: utf-8 -*-
"""
relay_commander.validator
~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides helper functions that validate CLI input.
"""


def validateState(state: str) -> bool:
    """Validate State Argument

    Checks that either 'on' or 'off' was entered as an argument to the
    CLI and make it lower case.

    :param state: state to validate.

    :returns: True if state is valid.
    """
    lowerCaseState = state.lower()

    if lowerCaseState == 'on' or lowerCaseState == 'off':
        return True
    else:
        return False
