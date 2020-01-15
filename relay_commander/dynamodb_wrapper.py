import boto3
import json
import sys

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


    def get_ddb_flag_record(self, feature_key: str) -> str:
        """Get feature flag record from dynamoDB.

        :param feature_key: key for feature flag

        :return: value of feature flag key in dynamoDB.

        :raises: KeyError if key is not found.
        """
        response = self.ddb_table.get_item(
            Key={
            'namespace': 'ld:{0}:{1}:features'.format(self.project_key, self.environment_key),
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
        """Update dynamoDB record with new state.

        :param state: state for feature flag.
        :param feature_key: key for feature flag.
        """
        item = self.get_ddb_flag_record(feature)
        try:
            item['on'] = state
            item['version'] += 1
            updated_item = json.dumps(item)
        except KeyError as ex:
            LOG.error(ex)
            sys.exit(1)

        LOG.info('updating %s to %s', feature, state)

        response = self.ddb_table.update_item(
            Key={
                'namespace': 'ld:{0}:{1}:features'.format(self.project_key, self.environment_key),
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
