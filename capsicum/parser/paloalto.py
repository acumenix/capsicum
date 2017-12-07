from .. import base


class PaloAlto(base.Stream):
    TRAFFIC_COLUMN = [
        'Domain', 'Receive Time', 'Serial #', 'Type', 'Threat/Content Type',
        'Config Version', 'Generate Time', 'Source address',
        'Destination address', 'NAT Source IP', 'NAT Destination IP', 'Rule',
        'Source User', 'Destination User', 'Application', 'Virtual System',
        'Source Zone', 'Destination Zone', 'Inbound Interface',
        'Outbound Interface', 'Log Action', 'Time Logged', 'Session ID',
        'Repeat Count', 'Source Port', 'Destination Port', 'NAT Source Port',
        'NAT Destination Port', 'Flags', 'IP Protocol', 'Action', 'Bytes',
        'Bytes Sent', 'Bytes Received', 'Packets', 'Start Time',
        'Elapsed Time (sec)', 'Category', 'Padding', 'seqno', 'actionflags',
        'Source Country', 'Destination Country', 'cpadding', 'pkts_sent',
        'pkts_received', 'session_end_reason', 'dg_hier_level_1',
        'dg_hier_level_2', 'dg_hier_level_3', 'dg_hier_level_4', 'vsys_name',
        'device_name', 'action_source'
    ]
    THREAT_COLUMN = [
        'Domain', 'Receive Time', 'Serial #', 'Type', 'Threat/Content Type',
        'Config Version', 'Generate Time', 'Source address',
        'Destination address', 'NAT Source IP', 'NAT Destination IP', 'Rule',
        'Source User', 'Destination User', 'Application', 'Virtual System',
        'Source Zone', 'Destination Zone', 'Inbound Interface',
        'Outbound Interface', 'Log Action', 'Time Logged', 'Session ID',
        'Repeat Count', 'Source Port', 'Destination Port', 'NAT Source Port',
        'NAT Destination Port', 'Flags', 'IP Protocol', 'Action', 'URL',
        'Threat/Content Name', 'Category', 'Severity', 'Direction', 'seqno',
        'actionflags', 'Source Country', 'Destination Country', 'cpadding',
        'contenttype', 'pcap_id', 'filedigest', 'cloud', 'url_idx',
        'user_agent', 'filetype', 'xff', 'referer', 'sender', 'subject',
        'recipient', 'reportid', 'dg_hier_level_1', 'dg_hier_level_2',
        'dg_hier_level_3', 'dg_hier_level_4', 'vsys_name', 'device_name',
        'file_url'
    ]

    COLUMN_MAP = {
        'TRAFFIC': TRAFFIC_COLUMN,
        'THREAT':  THREAT_COLUMN,
    }

    def receive(self, tag: str, timestamp: int, data: dict):
        msg = data.get('message')
        
        if msg:
            row = msg.split(',')
            if len(row) < 4:
                return

            column = PaloAlto.COLUMN_MAP.get(row[3])
            if not column:
                return  # unsupported log type
            
            if len(row) == len(column):
                data.update(dict(zip(column, row)))
                self.emit('paloalto.traffic', timestamp, data)
                return

        self.emit(tag, timestamp, data)
