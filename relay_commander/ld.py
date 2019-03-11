# -*- coding: utf-8 -*-
"""
relay_commander.ld
~~~~~~~~~~~~~~~~~~

This module provides a wrapper for the LaunchDarkly API.

Reference API - https://pypi.org/project/launchdarkly-api/

.. versionchanged:: 0.0.12
    Refactor module to make it PEP-8 and PEP-484 compliant.
"""
import sys

import launchdarkly_api

from relay_commander.util import LOG


class LaunchDarklyApi():
    """Wrapper for the LaunchDarkly API"""

    def __init__(
            self,
            api_key: str,
            project_key: str = None,
            environment_key: str = None
        ):
        """
        Instantiate a new LaunchDarklyApi instance.

        :param api_key: API Access Key for LaunchDarkly.
        :param project_key: Key for project.
        :param environment_key: Environment in which to \
            pull state from.
        """
        self.api_key = api_key
        self.project_key = project_key
        self.environment_key = environment_key

        # get new LD client
        configuration = launchdarkly_api.Configuration()
        configuration.api_key['Authorization'] = api_key
        self.client = launchdarkly_api.ProjectsApi(
            launchdarkly_api.ApiClient(configuration))
        self.feature = launchdarkly_api.FeatureFlagsApi(
            launchdarkly_api.ApiClient(configuration))


    def get_environments(self, project_key: str) -> dict:
        """
        Retrieve all environments for a given project.

        Includes name, key, and mobile key.

        :param project_key: Key for project.

        :returns: dictionary of environments.
        """
        try:
            resp = self.client.get_project(project_key)
        except launchdarkly_api.rest.ApiException as ex:
            msg = "Unable to get environments."
            resp = "API response was {0} {1}.".format(ex.status, ex.reason)
            LOG.error("%s %s", msg, resp)
            sys.exit(1)

        envs = []

        for env in resp.environments:
            env = dict(
                key=env.key,
                api_key=env.api_key,
                client_id=env.id
            )
            envs.append(env)

        return envs

    def update_flag(self, state: str, feature_key: str) \
        -> launchdarkly_api.FeatureFlag:
        """
        Update the flag status for the specified feature flag.

        :param state: New feature flag state
        :param featureKey: Feature flag key

        :returns: FeatureFlag object.
        """
        build_env = "/environments/" + self.environment_key + "/on"
        patch_comment = [{"op": "replace", "path": build_env, "value": state}]

        try:
            resp = self.feature.patch_feature_flag(
                self.project_key, feature_key, patch_comment)
        except launchdarkly_api.rest.ApiException as ex:
            msg = "Unable to update flag."
            resp = "API response was {0} {1}.".format(ex.status, ex.reason)
            LOG.error("%s %s", msg, resp)
            sys.exit(1)

        return resp
