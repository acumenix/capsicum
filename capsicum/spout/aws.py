#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import boto3
import gzip
import json

import logging

logger = logging.getLogger(name=__name__)
logger.setLevel(logging.DEBUG)


def get_all_objects(client, bucket_name, prefix):
    objects = []
    marker = ''

    while True:
        res = client.list_objects(Bucket=bucket_name, Prefix=prefix,
                                  Marker=marker)
        truncated = res.get('IsTruncated')
        contents  = res.get('Contents')
        marker    = res.get('Marker')
        if truncated is None or contents is None or marker is None:
            raise Exception('Invalid response from S3 API')

        objects += contents
        
        if truncated is False:
            return objects


class DatePrefix:
    def __init__(self, start_dt, fmt):
        self._dt = start_dt
        self._fmt = fmt
        self._prev = None
        
    def next_prefix(self):
        delta = datetime.timedelta(minutes=1)
        while True:
            prefix = self._dt.strftime(self._fmt)
            if self._prev != prefix:
                self._prev = prefix
                return prefix
            self._dt += delta

class FluentdS3:
    def __init__(self, bucket_name):
        self._bucket_name = bucket_name

    @property
    def name(self):
        return self.__class__.__name__

    def read(self, start_dt, end_dt):
        if ('AWS_ACCESS_KEY_ID' in os.environ and
            'AWS_SECRET_ACCESS_KEY' in os.environ):
            key_id = os.environ['AWS_ACCESS_KEY_ID']
            access_key = os.environ['AWS_SECRET_ACCESS_KEY']
            client = boto3.client('s3', aws_access_key_id=key_id,
                                  aws_secret_access_key=access_key)
        else:
            client = boto3.Session().client('s3')
            
        
        dt = start_dt
        # 2017-11-20T11:47:06+00:00
        dt_fmt = '%Y-%m-%dT%H:%M:%S+00:00'
        prefix_fmt = os.environ.get('TEST_S3_KEY_FMT') or 'logs/%Y/%m/%d'
        tzdiff     = int(os.environ.get('TEST_S3_LOG_TZ')) or 0

        in_time = True
        dp = DatePrefix(start_dt, prefix_fmt)
        log_tz = datetime.timezone(datetime.timedelta(hours=tzdiff), 'LOG')
        
        while in_time:
            prefix = dp.next_prefix()

            logger.info('Prefix', prefix)

            obj_list = get_all_objects(client, self._bucket_name, prefix)
            logger.info('s3 list object number:', len(obj_list))
            
            for obj in sorted(obj_list, key=lambda x: x['LastModified']):
                if obj['LastModified'] < start_dt:
                    continue
                
                data = client.get_object(Bucket=self._bucket_name,
                                         Key=obj['Key'])
                chunk = data['Body'].read()
                text = gzip.decompress(chunk).decode('utf8')
                
                for line in text.split('\n'):
                    row = line.strip().split('\t')
                    
                    if len(row) != 3: # Unexpected format, ignore
                        continue

                    jdata = json.loads(row[2])
                    obj_dt_naive = datetime.datetime.strptime(row[0], dt_fmt)
                    obj_dt = obj_dt_naive.replace(tzinfo=log_tz)

                    if start_dt <= obj_dt and obj_dt < end_dt:
                        jdata.update({ '@datetime': obj_dt, '@tag': row[1] })
                        yield jdata

                    if end_dt < obj_dt:
                        in_time = False
                        break

                if not in_time:
                    break
