#!/usr/bin/env python
# -*- coding: utf-8 -*-


import boto3

from ..helper import TEST_PREF
from capsicum.spout import aws
import capsicum
import pytest

# TEST_BUCKET


@pytest.mark.skipif(not TEST_PREF, reason='no test config')
def test_s3():
    prefix = TEST_PREF['aws']['s3'].get('prefix')
    postfix = 'syslog-sshd'
    if prefix:
        key = '{}/{}'.format(prefix, postfix)
    else:
        key = postfix

    q = capsicum.notify.Queue()
        
    spout = aws.S3(bucket=TEST_PREF['aws']['s3']['bucket'],
                   prefix=key)
    spout.pipe(q)
    spout.drain()

    assert len(q) > 0
    for tag, ts, data in q:
        assert ('Nov 23 ' in data['message'] or
                'Nov 25 ' in data['message'])
