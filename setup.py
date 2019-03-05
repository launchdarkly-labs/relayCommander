#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:copyright: (c) 2018-2019 by LaunchDarkly
:license: Apache 2.0, see LICENSE for more details.
"""
import os
import sys

from setuptools import setup
from setuptools.command.install import install

# relayCommander version
VERSION = "0.0.11"


def readme():
    """print long description"""
    with open('README.rst') as f:
        return f.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this \
                app: {1}".format(tag, VERSION)
            sys.exit(info)


setup(
    name="relaycommander",
    version=VERSION,
    description="CLI to Update LD Relay in Disaster Scenarios",
    long_description=readme(),
    url="https://github.com/launchdarkly/relayCommander",
    author="LaunchDarkly",
    author_email="sales@launchdarkly.com",
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: System :: Recovery Tools",
        "Topic :: System :: Systems Administration",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords='launchdarkly api redis relay',
    packages=['relay_commander'],
    install_requires=[
        'click',
        'click_log',
        'requests',
        'redis',
        'jinja2',
        'launchdarkly-api'
    ],
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires='~=3.5',
    cmdclass={
        'verify': VerifyVersionCommand,
    },
    entry_points='''
        [console_scripts]
        rc=relay_commander.rc:cli
    '''
)
