def validateState(state):
    """Checks that either true or false was entered and make it lower case

    :param state: State to validate
    """
    lowerCaseState = state.lower()
    
    if lowerCaseState == 'true' or lowerCaseState == 'false':
        return True
    else:
        return False