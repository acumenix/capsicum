import abc
import enum

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


class Rule(abc.ABC):    
    class result(enum.Enum):
        NORMAL = None
        ALERT = 1

    def __init__(self):
        self._blacklist = None
        
    def set_blacklist(self, blacklist):
        self._blacklist = blacklist

    def lookup_addr(self, key):
        if self._blacklist:
            return self._blacklist.lookup(key)
        else:
            return None

    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def assess(self, tag: str, timestamp: int, data: dict):
        pass

    @abc.abstractmethod
    def acceptable_tags(self):
        pass

    
