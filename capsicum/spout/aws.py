#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .. import base

import datetime
import os
import boto3
import botocore

import gzip
import json
import multiprocessing as mp
import pprint
import logging

logger = logging.getLogger(name=__name__)
logger.setLevel(logging.DEBUG)



def download(args):
    client = boto3.Session().client('s3')
    bucket = args['bucket']
    key    = args['key']

    data = client.get_object(Bucket=bucket, Key=key)
    if data['ContentLength'] == 0:
        return None
    
    chunk = data['Body'].read()
    if key.endswith('.gz'):
        text = gzip.decompress(chunk).decode('utf8')
    else:
        text = chunk.decode('utf8')

    return text
    

class S3(base.Spout):
    WORKER_NUM = 8
    
    def __init__(self, **kwargs):
        # must
        self._bucket = kwargs['bucket']
        # optional
        self._prefix = kwargs.get('prefix') or ''
            
    def drain(self):
        client = boto3.Session().client('s3')
        pool = mp.Pool(S3.WORKER_NUM)
        next_token = None
        truncated = True
        
        while truncated:
            query = {
                'Bucket': self._bucket,
                'Prefix': self._prefix,
            }
            if next_token:
                query['ContinuationToken'] = next_token
                
            res = client.list_objects_v2(**query)

            truncated = res['IsTruncated']
            contents  = res['Contents']
            next_token = res.get('NextContinuationToken')

            obj_list = [{'bucket': self._bucket, 'key': x['Key']}
                        for x in contents]

            for data in pool.imap(download, obj_list):
                if not data:
                    continue
                
                for line in data.split('\n'):
                    if len(line) > 0:
                        self.emit(None, None, {'message': line.strip()})



