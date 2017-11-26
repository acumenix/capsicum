import capsicum


def test_file():
    spout = capsicum.spout.local.File(path='tests/spout/data/sshd.log')
    q = capsicum.notify.Queue()
    spout.pipe(q)
    spout.drain()
    
    log = 'Nov 23 11:35:02 pylon sshd[8142]: pam_unix(sshd:auth): ' \
          'check pass; user unknown'

    assert len(q.queue) == 20
    assert q.queue[0]['message'] == log
