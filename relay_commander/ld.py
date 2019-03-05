"""ld module

Wrapper for the LaunchDarkly API

Reference API - https://pypi.org/project/launchdarkly-api/
"""
import launchdarkly_api


class LaunchDarklyApi():
    """Wrapper for the LaunchDarkly API"""

    def __init__(self, apiKey, projectKey=None, environmentKey=None, logger=None):
        """Instantiate a new LaunchDarklyApi instance.

        :param apiKey: API Access Key for LaunchDarkly
        :param projectKey: Key for project
        :param environmentKey: Environment in which to pull state from
        :param featureKey: Feature flag key to pull state from
        """
        self.apiKey = apiKey
        self.projectKey = projectKey
        self.environmentKey = environmentKey
        self.logger = logger

        # get new LD client
        configuration = launchdarkly_api.Configuration()
        configuration.api_key['Authorization'] = apiKey
        self.client = launchdarkly_api.ProjectsApi(
            launchdarkly_api.ApiClient(configuration))
        self.feature = launchdarkly_api.FeatureFlagsApi(
            launchdarkly_api.ApiClient(configuration))

    def formatHostname(self, key):
        """Returns formatted hostname for an environment.

        :param key: environment key
        """
        return "{0}".format(key)

    def getEnvironments(self, projectKey):
        """Returns List of Environments for a Project.

        Includes name, key, and mobile key, and formatted hostname.

        :param projectKey: Key for project

        :returns: Collection of Environments
        """
        resp = self.client.get_project(projectKey)
        envs = []

        for env in resp.environments:
            env = dict(
                key=env.key,
                api_key=env.api_key,
                client_id=env.id,
                hostname=self.formatHostname(env.key)
            )
            envs.append(env)

        return envs

    def updateFlag(self, state, featureKey):
        """Update the flag status for the specified feature flag

        :param state: New feature flag state
        :param featureKey: Feature flag key

        :returns: boolean status of the feature flag attribute "on"
        """
        buildEnv = "/environments/" + self.environmentKey + "/on"
        patchComment = [{"op": "replace", "path": buildEnv, "value": state}]

        return self.feature.patch_feature_flag(
            self.projectKey,
            featureKey,
            patchComment
            )
