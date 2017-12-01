from .. import base

from .snort import EmergingThreat
from .sslbl import SSLBL

from . import blacklist


class BlackList:
    def __init__(self, backend='memory', **kwargs):
        self._plugins = [
            EmergingThreat(),
            SSLBL(),
        ]

        self._repo = {
            'memory': blacklist.Memory,
            'json': blacklist.JsonFile,
        }[backend](**kwargs)

    def load(self):
        self._backend.load(self._repo)
        
    def sync(self):
        for p in self._plugins:
            p.fetch(self._repo)

        self._repo.sync()

    def lookup(self, key):
        if key:
            return self._repo.get(key)
        else:
            return None
