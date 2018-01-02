import sys
import os
import tempfile


bpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     '..', '..', 'capsicum', 'blacklist')
sys.path.append(bpath)

import blacklist


def set_repo_data(r):
    r.put('10.0.0.1', 'cnc', 'a', 10000)
    r.put('10.0.0.1', 'spam', 'a', 20000)
    r.put('10.0.0.2', 'bot', 'b', 30000)
    r.put('10.0.0.3', 'cnc', 'c', 40000)


def tsort(x):
    return sorted(x, key=lambda x: x['timestamp'])


def test_json_file():
    tmp = tempfile.mkstemp()
    os.close(tmp[0])

    r1 = blacklist.JsonFile(path=tmp[1])
    r2 = blacklist.JsonFile(path=tmp[1])
    set_repo_data(r1)

    assert len(r1) == 3
    assert len(r2) == 0
    
    r1.save()
    r2.load()

    assert len(r1) == len(r2)

    for k, arr in r2.items():
        for o1, o2 in zip(tsort(arr), tsort(r1[k])):
            assert o1['timestamp'] == o2['timestamp']

    os.remove(tmp[1])

import pprint

def test_dynamo_db():
    TABLE_NAME = 'capsicum-test-domain'
    r1 = blacklist.DynamoDB(region='ap-northeast-1', table=TABLE_NAME)
    r1.put('example.com', 'cnc', 'a', 10000)
    r1.put('example.org', 'spam', 'a', 20000)
    r1.put('example.net', 'bot', 'b', 30000)
    r1.put('example.xxx', 'cnc', 'c', 40000)
    r1.save()

    r2 = blacklist.DynamoDB(region='ap-northeast-1', table=TABLE_NAME)
    res = r2.get('example.org')
    assert res['reason'] == 'spam'
    
    res = r2.get('notfound.com')
    assert res is None

    
