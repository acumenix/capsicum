import capsicum


def test_top():
    spout = capsicum.spout.local.File(path='tests/spout/data/sshd.log')
    parser = capsicum.parser.SSHD()
    blist = capsicum.BlackList('json', path='tests/data/blist.json')
    notify_queue = capsicum.notify.Queue()
    
    spout.pipe(parser).pipe(blist).pipe(notify_queue)
    spout.drain()

    assert len(notify_queue) == 1
    
    tag, timestamp, data = notify_queue[0]
    assert tag == 'sshd.auth'
    assert data['remote_addr'] == '172.16.4.3'
