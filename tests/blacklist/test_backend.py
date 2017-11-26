import sys
import os
import tempfile
import pytest

bpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     '..', '..', 'capsicum', 'blacklist')
sys.path.append(bpath)

import blacklist


@pytest.fixture
def backend():
    r1 = blacklist.Repository()
    r2 = blacklist.Repository()
    r1.put('10.0.0.1', 'cnc', 'a', 10000)
    r1.put('10.0.0.1', 'spam', 'a', 20000)
    r1.put('10.0.0.2', 'bot', 'b', 30000)
    r1.put('10.0.0.3', 'cnc', 'c', 40000)
    
    return r1, r2


def test_json_file(backend):
    r1, r2 = backend
    tmp = tempfile.mkstemp()
    os.close(tmp[0])

    j1 = blacklist.JsonFile(path=tmp[1])
    j2 = blacklist.JsonFile(path=tmp[1])

    assert len(r1) == 3
    assert len(r2) == 0
    
    j1.dump(r1)
    j2.load(r2)

    assert len(r1) == len(r2)

    tsort = lambda x: sorted(x, key=lambda x: x['timestamp'])

    for k, arr in r2.items():
        for o1, o2 in zip(tsort(arr), tsort(r1[k])):
            assert o1['timestamp'] == o2['timestamp']

    os.remove(tmp[1])
