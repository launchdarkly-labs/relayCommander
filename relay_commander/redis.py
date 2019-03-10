# -*- coding: utf-8 -*-
"""
relay_commander.redis
~~~~~~~~~~~~~~~~~~~~~

This module provides an interface for working with redis.
"""
import json

import redis

_DEFAULT_REDIS_PORT = 6379
"""Internal constant that defines the default redis port."""


class _RedisConnection():
    """Private data class that represents a redis connection.

    :param host: hostname for redis
    :param port: port for redis

    .. versionchanged:: 0.0.12
        Refactored to become private, and renamed to fix typo.
    """

    def __init__(self, host: str, port: int):
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

    def _format_key_name(self) -> str:
        """Return formatted redis key name."""
        keyName = 'ld:{0}:{1}:features'.format(
            self.projectKey,
            self.environmentKey
        )
        return keyName

    @staticmethod
    def connectionStringParser(uri: str) -> list:
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
                port = _DEFAULT_REDIS_PORT
            elif len(rawConnection) == 2:
                host = rawConnection[0].strip()
                port = int(rawConnection[1])
            else:
                raise Exception("unable to parse redis connection string.")

            redisConnection = _RedisConnection(host, port)
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
