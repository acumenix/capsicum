from . import blacklist

import requests


class EmergingThreat(blacklist.Plugin):
    DEFAULT_BASE_URL = 'https://rules.emergingthreats.net/' \
                       'open/snort-edge/rules'
    DEFAULT_RULES = [
        'emerging-botcc.rules',
        'emerging-compromised.rules',
    ]

    def source_name(self):
        return 'EmergingThreat'

    @staticmethod
    def extract_addrs(line):
        s = line.strip()
        if s[0] == '[' and s[-1] == ']':
            ipaddr = s[1:-1].split(',')
        else:
            ipaddr = [s]

        return ipaddr

    def fetch(self):
        for rule_name in EmergingThreat.DEFAULT_RULES:
            url = '{}/{}'.format(EmergingThreat.DEFAULT_BASE_URL, rule_name)
            
            r = requests.get(url)
            for line in r.text.split('\n'):
                body_idx = line.find('(')
                hdr = line[:body_idx].split(' ')
                body = dict(filter(lambda x: len(x) == 2,
                                   [tuple(kv.strip().split(':'))
                                    for kv in line[(body_idx+1):].split(';')]))
                
                if hdr[0] != 'alert': continue

                ipaddr_list = []
                for idx in [2, 5]: # for src & dst addresses
                    if 'any' != hdr[idx] and hdr[idx][0] != '$':
                        ipaddr_list += EmergingThreat.extract_addrs(hdr[idx])

                for ipaddr in set(ipaddr_list):
                    self.put(ipaddr, body.get('msg'))
                           
        
