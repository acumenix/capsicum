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
