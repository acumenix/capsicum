import capsicum


class SshBadIPAddr(capsicum.Rule):
    def name(self):
        return 'sshd accepted access from bad IP address'
        
    def assess(self, tag: str, timestamp: int, data: dict):
        remote_addr = data.get('remote_addr')
        result = data.get('result')
        bad_addr = self.lookup_addr(remote_addr)

        if result == 'Accepted' and bad_addr:
            return capsicum.Rule.result.ALERT
        else:
            return capsicum.Rule.result.NORMAL

    def acceptable_tags(self):
        return ['sshd.auth']


class AccessToBadIPaddrAtFW(capsicum.Rule):
    def name(self):
        return 'Access to bad IP address'
    
    def acceptable_tags(self):
        return ['paloalto.traffic']
    
    def assess(self, tag: str, timestamp: int, data: dict):
        src_addr, dst_addr = None, None
        if tag == 'paloalto.traffic':
            dst_addr = data.get('Destination address')
            src_addr = data.get('Source address')

        if self.lookup_addr(src_addr) or self.lookup_addr(dst_addr):
            return capsicum.Rule.result.ALERT
        else:
            return capsicum.Rule.result.NORMAL
            
            
