# relayCommander
Python CLI to Update LD Relay in Disaster Scenarios

## Vision?
rc update $PROJECT $ENV $FEATURE $STATE

    1. Updates Redis (including version #)
    2. Starts a long poll to update LD as soon as it comes back online.

## Usage

pip install relayCommander

## Libraries

[Click](https://click.palletsprojects.com/en/7.x/)
[Redis](https://pypi.org/project/redis/)
[LD API](https://github.com/launchdarkly/ld-openapi)