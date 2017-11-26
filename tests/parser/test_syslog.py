import capsicum


def test_sshd_log():
    spout = capsicum.spout.local.File(path='tests/spout/data/sshd.log')
    q = capsicum.notify.Queue()
    
    spout.pipe(capsicum.parser.SSHD()).pipe(q)
    spout.drain()
    assert len(q) == 4
