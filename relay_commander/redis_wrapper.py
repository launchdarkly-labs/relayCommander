# -*- coding: utf-8 -*-
"""
relay_commander.redis
~~~~~~~~~~~~~~~~~~~~~

This module provides an interface for working with redis.

.. versionchanged: 0.0.12
    * refactor to conform with pep-8 and pep-484
    * renamed file to redis_wrapper to reduce confusion about which redis
      we are importing.
    * clean up exception handling, and raise more specific exceptions.
"""
import json
import sys

import redis

from relay_commander.util import LOG

_DEFAULT_REDIS_PORT = 6379
"""Internal constant that defines the default redis port."""


class _RedisConnection():
    """
    Private data class that represents a redis connection.

    :param host: hostname for redis
    :param port: port for redis

    .. versionchanged:: 0.0.12
        Refactored to become private, and renamed to fix typo.
    """

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port


class RedisWrapper():
    """
    A wrapper around the redis library.

    This class implements some general data access patterns as well as
    LaunchDarkly relay specific functionality.

    :param host: redis hostname.
    :param port: redis port.
    :param project_key: LaunchDarkly project key
    :param environment_key: LaunchDarkly environment key.
    """

    def __init__(self, host, port, project_key, environment_key):
        self.project_key = project_key
        self.environment_key = environment_key
        self.redis = redis.Redis(host=host, port=port)

    def _format_key_name(self) -> str:
        """Return formatted redis key name."""
        key_name = 'ld:{0}:{1}:features'.format(
            self.project_key,
            self.environment_key
        )
        return key_name

    @staticmethod
    def connection_string_parser(uri: str) -> list:
        """
        Parse Connection string to extract host and port.

        :param uri: full URI for redis connection in the form of
        host:port

        :returns: list of RedisConnection objects
        """
        redis_connections = []
        raw_connections = uri.split(',')
        connections = [
            connection for connection in raw_connections if len(connection) > 0
        ]

        for connection in connections:
            raw_connection = connection.split(':')
            if len(raw_connection) == 1:
                host = raw_connection[0].strip()
                port = _DEFAULT_REDIS_PORT
            elif len(raw_connection) == 2:
                host = raw_connection[0].strip()
                port = int(raw_connection[1])
            else:
                raise RuntimeError(
                    "Unable to parse redis connection string: {0}".format(
                        raw_connection
                    )
                )

            redis_connection = _RedisConnection(host, port)
            redis_connections.append(redis_connection)

        return redis_connections

    def get_flag_record(self, feature_key: str) -> str:
        """Get feature flag record from redis.

        :param feature_key: key for feature flag

        :return: value of feature flag key in redis.

        :raises: KeyError if key is not found.
        """
        key_name = self._format_key_name()
        flag = self.redis.hget(key_name, feature_key)

        if flag is None:
            raise KeyError('Redis key: {0} not found.'.format(key_name))

        return flag

    def update_flag_record(self, state: str, feature_key: str) -> None:
        """Update redis record with new state.

        :param state: state for feature flag.
        :param feature_key: key for feature flag.
        """
        key_name = self._format_key_name()
        try:
            parsed_flag = json.loads(self.get_flag_record(feature_key).decode('utf-8'))
            parsed_flag['on'] = state
            parsed_flag['version'] += 1
            updated_flag = json.dumps(parsed_flag).encode('utf-8')
        except KeyError as ex:
            LOG.error(ex)
            sys.exit(1)

        LOG.info('updating %s to %s', feature_key, state)

        self.redis.hset(key_name, feature_key, updated_flag)
