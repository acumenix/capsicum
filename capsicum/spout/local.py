#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import boto3


class SyslogFile:
    def __init__(self, fpath):
        self._fpath = fpath

    def read(self, start_dt, end_dt, **kwargs):
        for line in open(self._fpath, 'rt'):
            yield line
