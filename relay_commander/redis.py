import redis
import json

def updateRelay(ld, state):
    """Connects to a redis DB and updates the redis cache with the supplied state

    :param ld: ld is an instance of LaunchDarklyApi
    """
   
    #add envar for the host name of the redis server
    r = redis.Redis(host='52.39.223.175', port=6379, db=0, password='f8178631-c6a3-4cf3-abed-6eb149a15137')

    setKeyName = 'ld:' + ld.projectKey + ':' + ld.environmentKey + ':' + 'features'

    # 1 - get the value for the key
    getFlag = r.hget(setKeyName, ld.featureKey)

    # 2 - convert to dictionary
    parsedFlag = json.loads(getFlag)

    # 3 - update the value for the flag
    parsedFlag['on'] = state

    # 4 - increment the version number
    parsedFlag['version'] += 1

    # 5a- create a JSON string representation from the dictionary
    udpatedFlag = json.dumps(parsedFlag)

    # 5b- convert the string to bytes
    convertByte = udpatedFlag.encode('utf-8')

    # 6 - update the value for the key in the redis, being sure to use bytecode
    updateFlag = r.hset(setKeyName, ld.featureKey, convertByte)




if __name__ == '__main__':
    connectRedis()