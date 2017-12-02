from .. import base
import re
import datetime

SYSLOG_REGEX = re.compile('^(\S{3} \d{1,2} \d{2}:\d{2}:\d{2}) '
                          '(\S+) (\S+)\\[(\d+)\]:\s*(.*)$')


def syslog_parser(data):
    # Nov 21 06:00:24 ip-172-31-7-118 sshd[23511]:
    line = data.get('message')
    mo = SYSLOG_REGEX.search(line)
    if mo:
        data.update({
            'datetime':  mo.group(1),
            'hostname':  mo.group(2),
            'proc_name': mo.group(3),
            'proc_id':   mo.group(4),
            'message':   mo.group(5)
        })
        return data
    else:
        # unexpected format
        return data


class Syslog(base.Stream):
    BASE_DAY = datetime.datetime.now()
    
    def receive(self, tag: str, timestamp: int, data: dict):
        obj = syslog_parser(data)
        dt = datetime.datetime.strptime(obj['datetime'],
                                        '%b %d %H:%M:%S')
        self.emit(None, dt.timestamp(), obj)
