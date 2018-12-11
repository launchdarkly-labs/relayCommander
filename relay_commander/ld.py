"""ld module

Wrapper for the LaunchDarkly API

Note that the API SDK is generated using swagger. The entire library is
stored in the lib/ directory since we do not currently publish this anywhere.
"""
import launchdarkly_api
import json


class LaunchDarklyApi():
    """Wrapper for the LaunchDarkly API"""

    def __init__(self, apiKey, projectKey, environmentKey, featureKey):
        """Instantiate a new LaunchDarklyApi instance.

        :param apiKey: API Access Key for LaunchDarkly
        :param projectKey: Key for project
        :param environmentKey: Environment in which to pull state from
        :param featureKey: Feature flag key to pull state from
        """
        self.apiKey = apiKey
        self.projectKey = projectKey
        self.environmentKey = environmentKey
        self.featureKey = featureKey


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
                api_key = env.api_key,
                client_id = env.id,
                hostname = self.formatHostname(env.key)
            )
            envs.append(env)

        return envs

    def getFlagStatus(self):
        """Returns the status of a feaure flag.

        Includes name, key, and mobile key, and formatted hostname.

        :returns: boolean status of a feature flag
        """
        try:
            getFlag = self.feature.get_feature_flag(self.projectKey, self.featureKey)
            return getFlag.environments[self.environmentKey].on
        except launchdarkly_api.rest.ApiException as e:
            # getError = launchdarkly_api.rest.ApiException()
            # print("Something went wrong")
            print(e.getMessage())
        

        # getFlag = self.feature.get_feature_flag(projectKey, featureKey)
        # return getFlag.environments[environmentKey].on
    
    def updateFlag(self, state):
        buildEnv = "/environments/"+ self.environmentKey + "/on"
        patchComment = [{ "op": "replace", "path": buildEnv, "value": state }]

        return self.feature.patch_feature_flag(self.projectKey, self.featureKey, patchComment)
        

    def callText(self):
        return print("something is happening!")