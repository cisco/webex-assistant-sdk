#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module contains the specification of the mindmeld package"""
# pylint: disable=locally-disabled,invalid-name
from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'cryptography>=2.8,<3.1',
    'mindmeld~=4.2'
]

setup_requirements = [
    'pytest-runner~=2.11',
    'setuptools>=36'
]

test_requirements = [
    'flake8==3.5.0',
    'pylint==1.6.5',
    'pytest==3.8.0',
    'pytest-cov==2.4.0',
    'pytest-asyncio==0.8.0'
]

setup(
    name='webex_assistant_sdk',
    version='0.1.0',
    description="SDK for developing applications for Webex Assistant.",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="Cisco Systems, Inc.",
    author_email='contact@mindmeld.com',
    url='https://github.com/cisco/mindmeld',
    packages=[
        'webex_assistant_sdk',
    ],
    package_dir={'webex_assistant_sdk': 'webex_assistant_sdk'},
    include_package_data=False,
    install_requires=requirements,
    zip_safe=False,
    keywords=['mindmeld', 'nlp', 'ai', 'conversational', 'webex', 'webex-assistant'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: Apache Software License'
    ],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
)
