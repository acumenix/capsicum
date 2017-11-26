from .. import base

from .snort import EmergingThreat
from .sslbl import SSLBL

from . import blacklist


class BlackList(base.Stream):
    def __init__(self, backend='memory', **kwargs):
        self._plugins = [
            EmergingThreat(),
            SSLBL(),
        ]

        self._repo = blacklist.Repository()
        for p in self._plugins:
            p.set_repository(self._repo)
    
        self._backend = {
            'memory': None,
        }[backend]

    def sync(self):
        for p in self._plugins:
            p.fetch()
        
    def receive(self, tag: str, timestamp: int, data: dict):
        self.emit(tag, timestamp, data)
