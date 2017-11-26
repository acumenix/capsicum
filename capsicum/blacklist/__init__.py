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
    
        self._backend = {
            'memory': blacklist.Memory,
            'json': blacklist.JsonFile,
        }[backend](**kwargs)

    def load(self):
        self._backend.load(self._repo)
        
    def sync(self):
        for p in self._plugins:
            p.fetch(self._repo)

    def receive(self, tag: str, timestamp: int, data: dict):
        self.emit(tag, timestamp, data)
