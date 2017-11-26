import abc
import collections
import datetime

#
# Streaming processor
#

class Pipe(abc.ABC):
    def __init__(self):
        self._dst = None
        pass

    def pipe(self, dst):
        self._dst = dst
        return self._dst

    def emit(self, tag: str, timestamp: int, data: dict):
        if self._dst:
            self._dst.receive(tag, timestamp, data)
    

class Spout(Pipe, abc.ABC):
    @abc.abstractmethod
    def drain(self):
        pass

            
class Stream(Pipe, abc.ABC):
    @abc.abstractmethod
    def receive(self, tag: str, timestamp: int, data: dict):
        pass


# 
# BlackList management
#

class Repository(abc.ABC):
    def __init__(self):
        self._map = collections.defaultdict(list)

    def put(self, key, reason, source_name, timestamp=None):
        self._map[key].append({
            'reason': reason,
            'src': source_name,
            'timestamp': timestamp or datetime.datetime.now().timestamp(),
        })


class BlackListPlugin(abc.ABC):
    def __init__(self):
        self._rep = Repository()

    def set_repository(self, rep):
        self._rep = rep

    @abc.abstractmethod
    def source_name(self):
        raise NotImplemented()

    @abc.abstractmethod
    def fetch(self):
        raise NotImplemented()
    
    def put(self, key, reason):
        self._rep.put(key, reason, self.source_name())
        
