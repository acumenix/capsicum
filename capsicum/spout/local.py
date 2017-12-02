from .. import base


class File(base.Spout):
    def __init__(self, **kwargs):
        self._path = kwargs['path']

    def drain(self):
        for line in open(self._path, 'rt'):
            self.emit(None, None, {'message': line.strip()})
