from . import blacklist

import requests


class SSLBL(blacklist.Plugin):
    DEFAULT_URL = 'https://sslbl.abuse.ch/blacklist/sslipblacklist_aggressive.csv'
    
    def fetch(self, repo):
        r = requests.get(SSLBL.DEFAULT_URL)
        for line in r.text.split('\n'):
            if line[0] == '#':
                continue

            row = line.split(',')
            repo.put(row[0], 'port {}, {}'.format(row[1], row[2]), 'SSLBL')
