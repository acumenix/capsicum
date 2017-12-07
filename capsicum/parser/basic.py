from .. import base
import json


class Json(base.Stream):
    def receive(self, tag: str, timestamp: int, data: dict):
        msg = data.get('message')
        try:
            self.emit(tag, timestamp, json.loads(msg))
        except json.decoder.JSONDecodeError:
            self.emit(tag, timestamp, data)
