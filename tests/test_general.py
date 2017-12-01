import capsicum


def test_top():
    spout = capsicum.spout.local.File(path='tests/spout/data/sshd.log')
    parser = capsicum.parser.SSHD()
    
    blist = capsicum.BlackList('json', path='tests/data/blist.json')
    
    engine = capsicum.RuleEngine()
    engine.set_blacklist(blist)
    engine.load_rule_dir('./rules')
    
    notify_queue = capsicum.notify.Queue()
    
    spout.pipe(parser).pipe(engine).pipe(notify_queue)
    spout.drain()

    assert len(notify_queue) == 1
    
    tag, timestamp, data = notify_queue[0]
    assert tag == 'sshd.auth'
    assert data['remote_addr'] == '10.2.3.4'
