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

    @abc.abstractmethod
    def sync(self):
        raise NotImplemented()

    
class Plugin(abc.ABC):
    @abc.abstractmethod
    def fetch(self, repository):
        raise NotImplemented()

    def put(self, key, reason):
        self._rep.put(key, reason, self.source_name())
        

class Memory(Repository):
    def sync(self):
        pass
    
    
class JsonFile(Repository):
    def __init__(self, **kwargs):
        super().__init__()
        self._path = kwargs['path']
        self.load()

    def sync(self):
        # assume that json file is not changed by any other process
        self.save()
        
    def load(self):
        for line in open(self._path, 'rt'):
            row = line.strip().split('\t')
            key = row[0]
            o = json.loads(row[1])
            self.put(key, o['reason'], o['src'], o['timestamp'])
            
    def save(self):
        fd = open(self._path, 'wt')
        for key, arr in self.items():
            for o in arr:
                fd.write('{}\t{}\n'.format(key, json.dumps(o)))
