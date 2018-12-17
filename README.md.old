# relayCommander
Python CLI to Update LD Relay in Disaster Scenarios

## Quickstart

1. Make sure you have [pipenv](https://pipenv.readthedocs.io/en/latest/install/) installed locally.
2. Clone this repo and run `pipenv install -e.`
3. Run some cli commands with `pipenv run rc`

---

# Design Notes
## Vision?
rc update $PROJECT $ENV $FEATURE $STATE

    1. Updates Redis (including version #)
    2. Starts a long poll to update LD as soon as it comes back online.

## Usage

pip install relayCommander

## Runbook
Need to have the following pre-reqs and LD is offline:
- Running on AWS
- Change rule to deny all outbound traffic from relay proxy
- Update Redis by running command rc update
- Restart relay proxy server and changes will take effect

Once LaunchDarkly is back online
- Replay the updates that were made by running rc replay
- Update the rule on AWS to allow outbound traffic again
- Restart the relay box
- Verify that making a change to a feature flag box

## Libraries

[Click](https://click.palletsprojects.com/en/7.x/)
[Redis](https://pypi.org/project/redis/)
[LD API](https://github.com/launchdarkly/ld-openapi)