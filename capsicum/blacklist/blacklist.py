import abc
import collections
import datetime
import json

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

    def items(self):
        return self._map.items()

    def __len__(self):
        return len(self._map)

    def __bool__(self):
        return True

    def __getitem__(self, key):
        return self._map[key]

    
class Plugin(abc.ABC):
    @abc.abstractmethod
    def source_name(self):
        raise NotImplemented()

    @abc.abstractmethod
    def fetch(self, repository):
        raise NotImplemented()
    
    def put(self, key, reason):
        self._rep.put(key, reason, self.source_name())
        

class Backend(abc.ABC):
    @abc.abstractmethod
    def load(self, repository):
        raise NotImplemented()

    @abc.abstractmethod
    def save(self, repository):
        raise NotImplemented()
    

class Memory(Backend):
    def __init__(self, **kwargs):
        self._repo = None

    def load(self, repository):
        if self._repo:
            for key, arr in self._repo.items():
                for o in arr:
                    repository.put(key, o['reason'], o['src'], o['timestamp'])
            
    def save(self, repository):
        self._repo = repository
    
    
class JsonFile(Backend):
    def __init__(self, **kwargs):
        self._path = kwargs['path']

    def load(self, repository):
        for line in open(self._path, 'rt'):
            row = line.strip().split('\t')
            key = row[0]
            o = json.loads(row[1])
            repository.put(key, o['reason'], o['src'], o['timestamp'])
            
    def save(self, repository):
        fd = open(self._path, 'wt')
        for key, arr in repository.items():
            for o in arr:
                fd.write('{}\t{}\n'.format(key, json.dumps(o)))
