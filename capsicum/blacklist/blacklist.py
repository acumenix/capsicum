import abc
import collections
import datetime


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

    def __len__(self):
        return len(self._map)

    def __bool__(self):
        return True


class Plugin(abc.ABC):
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
        

class Backend:
    @abc.abstractmethod
    def load(self, repository):
        raise NotImplemented()

    @abc.abstractmethod
    def sync(self, repository):
        raise NotImplemented()
    

