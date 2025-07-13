#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'base58>=1.0.2,<2.0',
    'py-multibase>=1.0.0,<2.0.0',
    'py-multicodec<0.3.0',
    'morphys>=1.0,<2.0',
    'pymultihash>=0.8.0,<1.0.0',
]

setup(
    name='py-cid',
    version='0.3.0',
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
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
