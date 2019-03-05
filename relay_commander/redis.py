"""
relay_commander.redis

A Redis Wrapper
"""
import json

import redis

DEFAULT_REDIS_PORT = 6379


class RedisConention():
    """Redis Connetion

    :param host: hostname for redis
    :param port: port for redis
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port


class RedisWrapper():
    """Relay Specific Redis Wrapper.

    :param projectKey: LaunchDarkly project key
    :param environmentKey: LaunchDarkly environment key.
    :param conn: (optional) redis connection string
    """

    def __init__(self, host, port, logger, projectKey, environmentKey):
        self.logger = logger
        self.projectKey = projectKey
        self.environmentKey = environmentKey
        self.redis = redis.Redis(host=host, port=port)

    def _formatKeyName(self):
        """Return formatted redis key name."""
        keyName = 'ld:{0}:{1}:features'.format(
            self.projectKey,
            self.environmentKey
        )
        return keyName

    @staticmethod
    def connectionStringParser(uri):
        """Parse Connection string to extract host and port.

        :param uri: full URI for redis connection in the form of
        host:port

        :returns: list of RedisConnection objects
        """
        redisConnections = []
        rawConnections = uri.split(',')
        connections = [
            connection for connection in rawConnections if len(connection) > 0
        ]

        for connection in connections:
            rawConnection = connection.split(':')
            if len(rawConnection) == 1:
                host = rawConnection[0].strip()
                port = DEFAULT_REDIS_PORT
            elif len(rawConnection) == 2:
                host = rawConnection[0].strip()
                port = int(rawConnection[1])
            else:
                raise Exception("unable to parse redis connection string.")

            redisConnection = RedisConention(host, port)
            redisConnections.append(redisConnection)

        return redisConnections

    def getFlagRecord(self, featureKey):
        """Get feature flag record from redis.

        :param featureKey: key for feature flag
        """
        keyName = self._formatKeyName()
        flag = self.redis.hget(keyName, featureKey)

        if flag is not None:
            return flag
        else:
            raise Exception('redis key not found.')

    def updateFlagRecord(self, state, featureKey):
        """Update redis record with new state.

        :param state: state for feature flag
        :param featureKey: key for feature flag
        """
        keyName = self._formatKeyName()
        parsedFlag = json.loads(self.getFlagRecord(featureKey).decode('utf-8'))
        parsedFlag['on'] = state
        parsedFlag['version'] += 1

        updatedFlag = json.dumps(parsedFlag).encode('utf-8')

        self.logger.info('updating {0} to {1}'.format(featureKey, state))

        self.redis.hset(keyName, featureKey, updatedFlag)
