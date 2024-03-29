#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from setuptools import setup

def _requires_from_file(filename):
    return open(filename).read().splitlines()

setup(
    name='capsicum',
    version='0.0.1',
    description='Lazy Event Risk Assessment Tool',
    author='Masayoshi Mizutani',
    author_email='mizutani@sfc.wide.ad.jp',
    install_requires=['requests', 'boto3'],
    test_requires=['pytest'],
    url='https://github.com/m-mizutani/capsicum',
    packages=['capsicum'],
    scripts=['bin/capsicum'],
)
