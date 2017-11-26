from .. import base


class BlackList(base.Stream):
    def __init__(self):
        pass
    
    def sync(self):
        pass
    
    def receive(self, tag: str, timestamp: int, data: dict):
        self.emit(tag, timestamp, data)
