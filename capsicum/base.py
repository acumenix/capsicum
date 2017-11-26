import abc
import typing


class Pipe(abc.ABC):
    def __init__(self):
        self._dst = None
        pass

    def pipe(self, dst) -> typing.TypeVar('Pipe'):
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
