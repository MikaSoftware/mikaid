#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import io
import re
import os
import sys


def readme():
    with io.open("README.md", "r", encoding="utf-8") as my_file:
        return my_file.read()

setup(
    name='mikaid',
    version='0.0.25',
    url='https://github.com/mikasoftware/mikaid',
    license='BSD 3-Clause License',
    description="A web framework for building user identity and access management (IAM) for all applications.",
    long_description=readme(),
    author='Bartlomiej Mika',
    author_email='bart@mikasoftware.com',
    packages=find_packages(),
    install_requires=[
        'django>=2.1.5',
        'djangorestframework>=3.9.0',
        'django-oauth-toolkit>=1.2.0'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities'
    ],
    keywords='library oauth',
)
