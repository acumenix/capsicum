#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import datetime
from capsicum.spout import aws


# TEST_BUCKET


''' DISABLED
def test_load_data():    
    spout = aws.FluentdS3(os.environ['TEST_S3_BUCKET'])
    iso_fmt = '%Y-%m-%dT%H:%M:%S'
    start_dt = datetime.datetime.strptime(os.environ['TEST_S3_START'], iso_fmt, )
    end_dt   = datetime.datetime.strptime(os.environ['TEST_S3_END'], iso_fmt)
    
    start_dt = start_dt.replace(tzinfo=datetime.timezone.utc)
    end_dt   = end_dt.replace(tzinfo=datetime.timezone.utc)

    count = 0
    for ev in spout.read(start_dt, end_dt):
        assert 'message' in ev
        assert '@tag' in ev
        assert '@datetime' in ev
        assert start_dt <= ev['@datetime']
        assert ev['@datetime'] <= end_dt

        count += 1

    assert 0 < count
'''
