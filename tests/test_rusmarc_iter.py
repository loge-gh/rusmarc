import os
import io

from rusmarc import RusmarcFileIterator, MarcFileIterator, Rusmarc


def test_iter():
    with RusmarcFileIterator(
            os.path.join(os.path.dirname(__file__), "data/TEST1.ISO"),
            encoding='cp1251'
    ) as iterator:
        i = 0
        for _ in iterator:
            i += 1
        assert i == 81

    recs_test = {}
    recs_serialized = {}
    with MarcFileIterator(
            os.path.join(os.path.dirname(__file__), "data/TEST1.ISO")
    ) as iterator:
        i = 0
        for mrc in iterator:
            i += 1
            r = Rusmarc(mrc, encoding='cp1251')            
            assert mrc == r.serialize(encoding='cp1251')
            recs_test[r.fields[1][0]] = r
        assert i == 81
    with io.open(os.path.join(os.path.dirname(__file__), "data/TEST1.txt"),
                 encoding='utf-8') as result:
        rec = ''
        key = None
        for l in result.readlines():
            if l.startswith("001: "):
                key = l[5:-1]
            if l.strip() == '':
                assert key is not None
                recs_serialized[key] = rec
                rec = ''
                key = None
            else:
                rec += l
    for k, r in recs_serialized.iteritems():                
        assert r == recs_test[k].serialize_marc_txt(encoding="cp1251")


if __name__ == "__main__":
    test_iter()
