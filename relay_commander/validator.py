"""validator module

Helper functions to validate CLI input
"""


def validateState(state):
    """Validate State Argument

    Checks that either 'on' or 'off' was entered as an argument to the
    CLI and make it lower case.

    :param state: state to validate
    """
    lowerCaseState = state.lower()

    if lowerCaseState == 'on' or lowerCaseState == 'off':
        return True
    else:
        return False
