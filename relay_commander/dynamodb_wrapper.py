import boto3
import json
import sys
import os

from relay_commander.util import LOG

DDB_CLIENT = boto3.resource('dynamodb')
"""AWS boto3 client"""


class DdbWrapper():
    """
    A wrapper around the boto3 library.

    This class implements some general data access patterns as well as
    LaunchDarkly relay specific functionality.

    :param table: table name for DynamoDB.
    :param project_key: LaunchDarkly project key
    :param environment_key: LaunchDarkly environment key.
    """

    def __init__(self, table, project_key, environment_key):
        self.project_key = project_key
        self.environment_key = environment_key
        self.ddb_table = DDB_CLIENT.Table(table)
        self.ddb_namespace_prefix = os.environ.get("DDB_NAMESPACE_PREFIX")
    
    def _format_namespace(self) -> str:
        """Return formatted DynamoDB namespace."""
        if self.ddb_namespace_prefix:
            namespace = self.ddb_namespace_prefix
        else:
            namespace = 'ld:{0}:{1}:features'.format(self.project_key, self.environment_key)
        return namespace

    def get_ddb_flag_record(self, feature_key: str) -> str:
        """Get feature flag record from DynamoDB.

        :param feature_key: key for feature flag

        :return: value of feature flag key in DynamoDB.

        :raises: KeyError if key is not found.
        """
        response = self.ddb_table.scan()
        data = response['Items']
        namespace = self._format_namespace()
        while 'LastEvaluatedKey' in response:
            response = self.ddb_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])

        response = self.ddb_table.get_item(
            Key={
            'namespace': namespace,
            'key': feature_key
            } 
        )

        try:
            item = json.loads(response['Item'].get('item'))
        except:
            LOG.error('flag key: {0} not found.'.format(feature_key))
            sys.exit(1)
        return item

    def update_ddb_flag_record(self, feature, state):
        """Update DynamoDB record with new state.

        :param state: state for feature flag.
        :param feature_key: key for feature flag.
        """
        namespace = self._format_namespace()
        item = self.get_ddb_flag_record(feature)
        try:
            item['on'] = state
            item['version'] += 1
            updated_item = json.dumps(item)
        except KeyError as ex:
            LOG.error(ex)
            sys.exit(1)

        LOG.info('updating %s to %s with namespace:%s', feature, state, namespace)

        response = self.ddb_table.update_item(
            Key={
                'namespace': namespace,
                'key': feature
            },
            UpdateExpression='set #state = :r',
            ExpressionAttributeValues={
                ':r': updated_item,
            },
            ExpressionAttributeNames={
                '#state': 'item',
            }
        )
