import requests
import datetime

from .. import base


class SSLBL(base.BlackListPlugin):
    DEFAULT_URL = 'https://sslbl.abuse.ch/blacklist/sslipblacklist_aggressive.csv'
    
    def source_name(self):
        return 'SSLBL'
        
    def fetch(self):
        r = requests.get(SSLBL.DEFAULT_URL)
        for line in r.text.split('\n'):
            if line[0] == '#':
                continue

            row = line.split(',')
            self.put(row[0], 'port {}, {}'.format(row[1], row[2]))
