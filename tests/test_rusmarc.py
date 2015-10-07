import os
import pytest
from rusmarc import Rusmarc, RusmarcFileIterator

@pytest.fixture
def setup():
    pass


def test_parse():
    with RusmarcFileIterator(
        os.path.join(os.path.dirname(__file__), "data/TEST1.ISO"),
        encoding='cp1251'
    ) as iterator:
        i = 0
        for _ in iterator:
            i += 1
        assert i == 81

def test_serialize():
    pass

