def validateState(state):
    
    lowerCaseState = state.lower()

    if lowerCaseState == 'true' or lowerCaseState == 'false':
        return True
    else:
        return False



#1 solve is my input valid
#2 cast to boolean