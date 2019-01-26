RunBook
=======

RelayCommander is a CLI tool that is intended to allow you to manually make a change to feature flags should your applications lose connectivity with the LaunchDarkly service. You must have the LD Relay setup with Redis in order for the CLI tool to work. It works by manually updating the status of a flag directly within Redis, while at the same time recording each update that has taken place. Then, once connection has been re-established with LaunchDarkly, you will then run a command that will update your configuration back to our service via the API. This iteration allows you to change the state of a feature flag to either ON or OFF. Due to the current way that SDK’s work with redis,  this can only be used to update the status of a backend feature flag.

Setup
------
- Python 3.6.7 is required
- You can install relay commander with `pip install relaycommander`; this will enable the rc command globally. 
- LD Relay proxy with Redis is setup
- Backend SDK clients are connected to the relay box

Instructions
-------------

Pre-requisites
~~~~~~~~~~~~~~

* Create a .env file similar to the sample file and be sure to update the following:
    -- REDIS_HOSTS
        * Update the .env file to include the host name(s) of the redis instances. If there are multiple redis instances running, provide as a CSV list of host names
    -- LD_API_KEY
        * LaunchDarkly API token to be used when writing the updates back to LaunchDarkly. Note that the API token requires administrative proviliges in order to work

While there is a disconnect with LaunchDarkly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Update redis by running: 

::
    
    rc update -p project -e environment -f feature_flag -s state

* Project = the key of the project to be updated
* Environment = the key of the environment to be updated
* Feature = the key of the feature to be updated
* State = the state of the feature flag you would like to change it to. Currently allows you to set it to On or Off

Each time this command is run, we will create a new direcoty called playback with a file containing the corresponding that needs to be run using the API

* No changes required: Changes will take effect once the relay cache detects the update and will broadcast the update to the SDK clients
* (Optional) Restart the relay proxy to server to make the updates immediate

.. warning::
    NO CHANGES CAN BE MADE WHILE LAUNCHDARKLY IS A DISCONNECTED. IT IS RECOMMENDED THAT YOU EITEHR HAVE AN INTERNAL PROCESS SO THAT NO ONE MAKES UPDATES DURING THIS TIME OR YOU DISABLE ALL LOGINS VIA SSO

Once LD is reconnected
~~~~~~~~~~~~~~~~~~~~~~

Run the following command: 

::

    rc replay

Running this command will iterate through all of the files that were created during ``rc update`` and make the corresponding udpates in LaunchDakly via the API to synch it with the offline changes that were made

Verify that the current state in LaunchDarkly matches that last state that was set using RelayCommander