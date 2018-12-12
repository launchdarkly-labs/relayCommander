def validateState(state):
    
    lowerCaseState = state.lower()

    if lowerCaseState == 'true' or lowerCaseState == 'false':
        return True
    else:
        return False