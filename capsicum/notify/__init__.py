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

    def pop(self):
        if len(self._queue) > 0:
            self._queue.pop(0)
        else:
            return None
