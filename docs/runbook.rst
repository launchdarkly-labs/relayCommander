RunBook
=======

RelayCommander is a CLI tool that is intended to allow you to manually make a
change to feature flags should your applications lose connectivity with the
LaunchDarkly service. You must have the LD Relay setup with Redis or DynamoDB in order for
the CLI tool to work. It works by manually updating the status of a flag
directly within Redis or DynamoDB, while at the same time recording each update that has
taken place. Then, once connection has been re-established with LaunchDarkly,
you will then run a command that will update your configuration back to our
service via the API. This iteration allows you to change the state of a
feature flag to either ON or OFF. Due to the current way that SDK’s work with
Redis and DynamoDB,  this can only be used to update the status of a backend feature flag.

Setup
------
- You can install relay commander with ``pip install relaycommander``;
  this will enable the rc command globally.
- LD Relay proxy with Redis or DynamoDB is setup
- Backend SDK clients are connected to the relay box

Instructions
-------------

Pre-requisites
~~~~~~~~~~~~~~

* Create a ``.env`` file similar to the `sample file <https://github.com/launchdarkly/relayCommander/blob/master/.env.example>`_ and be sure to update the following with at least 1 data store:
    -- REDIS_HOSTS
        * Update the ``.env`` file to include the host name(s) and
          port of the redis instances. If there are multiple redis instances running, provide as a CSV list of host names.
    -- DynamoDB
        * The AWS credentials and region for DynamoDB are not part of the relayCommander configuration; they should be set using either the standard AWS environment variables or a local AWS configuration file, as documented for `the AWS CLI <https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html>`_.
    -- LD_API_KEY
        * LaunchDarkly API token to be used when writing the updates back to LaunchDarkly.Note that the API token requires administrative proviliges in order to work.
    

While there is a disconnect with LaunchDarkly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Update redis by running:

::

    rc update -d redis -p project -e environment -f feature_flag -s state

* Project = the key of the project to be updated
* Environment = the key of the environment to be updated
* Feature = the key of the feature to be updated
* State = the state of the feature flag you would like to change it to. Currently allows you to set it to on or off

Update DynamoDB by running:

::

    rc update -d dynamodb -p project -e environment -f feature_flag -s state -t table

* Project = the key of the project to be updated
* Environment = the key of the environment to be updated
* Feature = the key of the feature to be updated
* State = the state of the feature flag you would like to change it to. Currently allows you to set it to on or off
* Table = the DynamoDB table name

Each time the `update` is run, we will create a new direcoty called playback with a file containing the corresponding commands that need to be run using the API

* No changes required: Changes will take effect once the relay cache detects the update and will broadcast the update to the SDK clients
* (Optional) Restart the relay proxy to server to make the updates immediate

.. warning::
    NO CHANGES TO THE LAUNCHDARKLY PLATFORM CAN BE MADE WHILE LAUNCHDARKLY IS DISCONNECTED. IT IS RECOMMENDED THAT YOU EITHER HAVE AN INTERNAL PROCESS SO THAT NO ONE MAKES UPDATES DURING THIS TIME OR YOU DISABLE ALL LOGINS VIA SSO

Once LD is reconnected
~~~~~~~~~~~~~~~~~~~~~~

Run the following command:

::

    rc playback

• Running this command will iterate through all of the files that were created during ``rc update`` and make the corresponding udpates in LaunchDakly via the API to sync it with the offline changes that were made

• Verify that the current state in LaunchDarkly matches the last state that was set using RelayCommander
