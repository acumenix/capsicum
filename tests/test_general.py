import capsicum


def test_top():
    spout = capsicum.spout.local.File(path='tests/spout/data/sshd.log')
    parser = capsicum.parser.SSHD()
    blist = capsicum.BlackList()
    blist.sync()
    notify = capsicum.notify.Stdout()
    
    spout.pipe(parser).pipe(blist).pipe(notify)
    spout.start()

