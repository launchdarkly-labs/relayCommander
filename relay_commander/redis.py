import redis
import json
import os

def updateRelay(ld, state, featureKey):
    """Connects to a redis DB and updates the redis cache with the supplied state

    :param ld: ld is an instance of LaunchDarklyApi
    :param state: Updated state for feature flag
    :param featureKey: Feature key
    """
    r = redis.Redis(host=os.environ.get('REDIS_HOST'))
    
    setKeyName = 'ld:{0}:{1}:features'.format(ld.projectKey,ld.environmentKey)
    getFlag = r.hget(setKeyName, featureKey)
    parsedFlag = json.loads(getFlag)
    parsedFlag['on'] = state
    parsedFlag['version'] += 1
    udpatedFlag = json.dumps(parsedFlag)
    convertByte = udpatedFlag.encode('utf-8')
    
    r.hset(setKeyName, ld.featureKey, convertByte)