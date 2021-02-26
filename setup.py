#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'base58',
    'py-multibase',
    'py-multicodec',
    'morphys',
    'py-multihash',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
    'pytest-cov',
]

setup(
    name='py-cid',
    version='0.4.0',
    description="Self-describing content-addressed identifiers for distributed systems",
    long_description=readme + '\n\n' + history,
    author="Dhruv Baldawa",
    author_email='dhruv@dhruvb.com',
    url='https://github.com/ipld/py-cid',
    packages=find_packages(include=['cid']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='cid',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
