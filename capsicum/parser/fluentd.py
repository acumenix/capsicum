from .. import base

import dateutil
import json


class FluentdJson(base.Stream):
    def receive(self, tag: str, timestamp: int, data: dict): 
        msg = data.get('message')
        if msg:
            row = msg.split('\t')

            dt = dateutil.parser.parse(row[0])
            jdata = json.loads(row[2])
            data.update(jdata)
            
            self.emit(row[1], dt.timestamp(), data)
        else:            
            self.emit(tag, timestamp, data)
