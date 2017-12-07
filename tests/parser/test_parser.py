import capsicum


def test_syslog_log():
    spout = capsicum.spout.local.File(path='tests/spout/data/sshd.log')
    q = capsicum.notify.Queue()
    
    spout.pipe(capsicum.parser.Syslog()).pipe(q)
    spout.drain()
    assert len(q) == 20


def test_sshd_log():
    spout = capsicum.spout.local.File(path='tests/spout/data/sshd.log')
    q = capsicum.notify.Queue()
    
    spout.pipe(capsicum.parser.Syslog()).pipe(capsicum.parser.Sshd()).pipe(q)
    spout.drain()
    assert len(q) == 4


def test_paloalto_log():
    spout = capsicum.spout.local.File(
        path='tests/spout/data/paloalto-fluentd.log')
    q = capsicum.notify.Queue()
    
    spout.pipe(capsicum.parser.FluentdJson()) \
         .pipe(capsicum.parser.PaloAlto()).pipe(q)
    spout.drain()
    assert len(q) == 2
    tag, timestamp, data = q[1]
    assert tag == 'paloalto.traffic'
    assert timestamp == 1512087316
    assert data['Destination address'] == '10.9.14.27'
    assert data['Source address'] == '172.16.102.21'
    
