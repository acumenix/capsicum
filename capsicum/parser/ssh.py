from .. import base
import re


class Sshd(base.Stream):
    AUTH_REGEX = re.compile(
        '^(Failed|Accepted) (\S+) for (invalid user |)(\S+)'
        ' from (\S+) port (\d+) '
    )

    def receive(self, tag: str, timestamp: int, data: dict):
        mo = Sshd.AUTH_REGEX.search(data['message'])

        if mo:
            data.update({
                'result':      mo.group(1),
                'auth':        mo.group(2),
                'invalid':     mo.group(3),
                'username':    mo.group(4),
                'remote_addr': mo.group(5),
                'remote_port': mo.group(6),
            })
            self.emit('sshd.auth', timestamp, data)
