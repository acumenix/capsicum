import capsicum


def test_top():
    spout = capsicum.spout.local.File(path='tests/spout/data/sshd.log')
    parser = capsicum.parser.SSHD()
    blist = capsicum.BlackList('json', path='tests/data/blist.json')
    notify = capsicum.notify.Queue()
    
    spout.pipe(parser).pipe(blist).pipe(notify)
    spout.drain()

