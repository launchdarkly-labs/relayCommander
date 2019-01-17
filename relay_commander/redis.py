import json
import os

import redis


class RedisWrapper():
    """Relay Specific Redis Wrapper.
    
    :param projectKey: LaunchDarkly project key
    :param environmentKey: LaunchDarkly environment key.
    :param conn: (optional) redis connection string
    """
    def __init__(self, logger, projectKey, environmentKey, conn=None):
        self.logger = logger
        self.projectKey = projectKey
        self.environmentKey = environmentKey
        self.conn = conn or os.environ.get('REDIS_HOST')
        self.redis = redis.Redis(host=self.conn)

        self.logger.info('established redis connection', self.redis)

    def _formatKeyName(self):
        """Return formatted redis key name."""
        keyName = 'ld:{0}:{1}:features'.format(
            self.projectKey,
            self.environmentKey
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
        keyName = self._formatKeyName()
        parsedFlag = json.loads(self.getFlagRecord(featureKey))
        parsedFlag['on'] = state
        parsedFlag['version'] += 1

        updatedFlag = json.dumps(parsedFlag).encode('utf-8')

        self.logger.info('updating {0} to {1}'.format(featureKey, state))

        self.redis.hset(keyName, featureKey, updatedFlag)
