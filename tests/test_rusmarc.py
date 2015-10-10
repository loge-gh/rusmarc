import os

from rusmarc import Rusmarc


def test_serialize():
    with open(
        os.path.join(os.path.dirname(__file__), "data/TEST2.ISO"),
        "rb"
    ) as f:
        rec_b = f.read()
        rec = Rusmarc(rec_b, encoding='cp1251')
        rec_t = rec.serialize(encoding='cp1251')
        assert rec_b == rec_t


def test_serialize_bad():
    with open(
            os.path.join(os.path.dirname(__file__), "data/ur.iso"),
            "rb"
    ) as f:
        rec_b = f.read()
        rec = Rusmarc(rec_b, encoding='utf-8')
        rec_t = rec.serialize(encoding='utf-8')
        assert rec_b != rec_t        


if __name__ == "__main__":
    test_serialize()