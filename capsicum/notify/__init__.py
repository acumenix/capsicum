import pprint
from .. import base


class Stdout(base.Stream):
    def receive(self, event):
        pprint.pprint(event)

        
class Queue(base.Stream):
    def __init__(self):
        super().__init__()
        self._queue = []
        
    def receive(self, event):
        self._queue.append(event)

    @property
    def queue(self):
        return self._queue[:]
        
    def __iter__(self):
        return self

    def __next__(self):
        if len(self._queue) > 0:
            return self._queue.pop(0)
        else:
            raise StopIteration()

