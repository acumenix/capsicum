import importlib.machinery as imm
import os
import inspect
import collections

from ..base import Stream
from ..base import Rule


class RuleEngine(Stream):
    def __init__(self):
        self._rules = []
        self._route = collections.defaultdict(list)
        self._blacklist = None
        
    def load_rule(self, fpath):
        abs_path = os.path.abspath(fpath)
        mod = imm.SourceFileLoader(abs_path, fpath).load_module()

        rules = [m[1]() for m in inspect.getmembers(mod)
                 if inspect.isclass(m[1])]
        self._rules.extend(rules)

        for r in rules:
            if self._blacklist:
                r.set_blacklist(self._blacklist)
                
            for tag in r.acceptable_tags():
                self._route[tag].append(r)

    def load_rule_dir(self, dpath):
        for fname in os.listdir(dpath):
            if fname.endswith('.py'):
                fpath = os.path.join(dpath, fname)
                self.load_rule(fpath)

    def set_blacklist(self, blacklist):
        self._blacklist = blacklist
        for rule in self._rules:
            rule.set_blacklist(blacklist)
                
    #
    # Event processing
    #
    def receive(self, tag: str, timestamp: int, data: dict):
        for rule in self._route.get(tag, []):
            if rule.assess(tag, timestamp, data) == Rule.result.ALERT:
                if 'capsicum.rules' not in data:
                    data['capsicum.rules'] = []

                data['capsicum.rules'].append(rule.name())
                data['capsicum.alert'] =  True
                
                self.emit(tag, timestamp, data)
