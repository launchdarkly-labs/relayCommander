import json
import os

import redis


class RedisWrapper():
    """Relay Specific Redis Wrapper.
    
    :param ld: instance of LaunchDarklyApi
    :param conn: (optional) redis connection string
    """
    def __init__(self, ld=None, conn=None):
        self.ld = ld
        self.conn = conn or os.environ.get('REDIS_HOST')
        self.redis = redis.Redis(host=self.conn)

    def _formatKeyName(self):
        """Return formatted redis key name."""
        keyName = 'ld:{0}:{1}:features'.format(
            self.ld.projectKey,
            self.ld.environmentKey
        )
        return keyName
    
    def getFlagRecord(self, featureKey):
        """Get feature flag record from redis.

        :param featureKey: key for feature flag
        """
        keyName = self._formatKeyName()
        flag = self.redis.hget(keyName, featureKey)

        if flag != None:
            return flag
        else:
            raise Exception('redis key not found.')
        
    def updateFlagRecord(self, state, featureKey):
        """Update redis record with new state.

        :param state: state for feature flag 
        :param featureKey: key for feature flag
        """
        parsedFlag = json.loads(self.getFlagRecord(featureKey))
        parsedFlag['on'] = state
        parsedFlag['version'] += 1

        updatedFlag = json.dumps(parsedFlag).encode('utf-8')

        self.redis.hset(keyName, featureKey, updatedFlag)
