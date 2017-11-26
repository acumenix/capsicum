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

    def __getitem__(self, key):
        return self._queue[key]

    def __bool__(self):
        return True
    
    def __len__(self):
        return len(self._queue)
    
    def __iter__(self):
        return self

    def __next__(self):
        if len(self._queue) > 0:
            return self._queue.pop(0)
        else:
            raise StopIteration()

