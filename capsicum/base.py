import abc


class Pipe(abc.ABC):
    def __init__(self):
        self._dst = None
        pass

    def pipe(self, dst):
        self._dst = dst
        return self._dst

    def emit(self, data):
        if self._dst:
            self._dst.receive(data)
    

class Spout(Pipe, abc.ABC):
    @abc.abstractmethod
    def drain(self):
        pass

    def start(self):
        for d in self.drain():
            self.emit(d)

            
class Stream(Pipe, abc.ABC):
    @abc.abstractmethod
    def receive(self, data):
        pass
