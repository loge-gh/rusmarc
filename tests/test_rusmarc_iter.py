import os
import io
import pytest
from rusmarc import RusmarcFileIterator


def test_iter():
    recs_test = {}
    recs_serialized = {}
    rec = RusmarcFileIterator(
        os.path.join(os.path.dirname(__file__), "data/TEST1.ISO"),
        encoding='cp1251'
    )
    i = 0
    for r in rec:
        i += 1
        recs_test[r.fields[1][0]] = r
    assert i == 81
    with io.open(os.path.join(os.path.dirname(__file__), "data/TEST1.txt"),
                 encoding='utf-8') as result:
        rec = ''
        key = None
        for l in result.readlines():
            rec += l
            if l.startswith("001: "):
                key = l[5:-1]
            if l.strip() == '':
                assert key is not None
                recs_serialized[key] = rec
                rec = ''
                key = None
    for k, r in recs_serialized.iteritems():
        print recs_test[k].serialize_marc_txt()
        print r
        assert r == recs_test[k].serialize_marc_txt(encoding="cp1251")

