import capsicum


class SshBadIPAddr(capsicum.Rule):
    def name(self):
        return 'sshd accepted access from bad IP address'
        
    def assess(self, tag: str, timestamp: int, data: dict):
        remote_addr = data.get('remote_addr')
        result = data.get('result')
        bad_addr = self.lookup_addr(remote_addr)

        print(data, remote_addr, result, bad_addr)
        if result == 'Accepted' and bad_addr:
            return capsicum.Rule.result.ALERT
        else:
            return capsicum.Rule.result.NORMAL

    def acceptable_tags(self):
        return ['sshd.auth']
