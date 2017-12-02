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

    def receive(self, tag: str, timestamp: int, data: dict):
        msg = data.get('message')

        if msg:
            row = msg.split(',')
            obj = dict(zip(PaloAlto.TRAFFIC_COLUMN, row))
            data.update(obj)
            self.emit(tag or 'paloalto.traffic', timestamp, data)
        else:
            self.emit(tag, timestamp, data)

