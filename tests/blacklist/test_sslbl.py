import sys
import os
import capsicum


bpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     '..', '..', 'capsicum', 'blacklist')
sys.path.append(bpath)

import blacklist


def test_bleeding_edge():
    r = blacklist.Memory()
    b = capsicum.blacklist.SSLBL()

    b.fetch(r)
    assert len(r) > 0
