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


class SSHD(base.Stream):

    AUTH_REGEX = re.compile(
        '^(Failed|Accepted) (\S+) for (invalid user |)(\S+)'
        ' from (\S+) port (\d+) '
    )
    BASE_DAY = datetime.datetime.now()

    def receive(self, tag: str, timestamp: int, data: dict):
        obj = syslog_parser(data)        
        mo = SSHD.AUTH_REGEX.search(obj['message'])        

        if mo:
            obj.update({
                'result':      mo.group(1),
                'auth':        mo.group(2),
                'invalid':     mo.group(3),
                'username':    mo.group(4),
                'remote_addr': mo.group(5),
                'remote_port': mo.group(6),
            })
            dt = datetime.datetime.strptime(obj['datetime'],
                                            '%b %d %H:%M:%S')
            dt = dt.replace(year=SSHD.BASE_DAY.year)
            self.emit('sshd.auth', dt.timestamp(), obj)
