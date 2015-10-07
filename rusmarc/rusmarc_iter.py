import io
import os
from rusmarc import Rusmarc, MalformedRecord


class RusmarcFileIterator(object):
    def __init__(self, filename, encoding=None):
        self.__enc = encoding
        self.__f = io.open(filename, "rb")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__f.close()

    def __iter__(self):
        return self

    def next(self):
        rec_len_b = bytearray("00000")
        if self.__f.readinto(rec_len_b):
            try:
                rec_len = int(rec_len_b)
            except ValueError:
                raise MalformedRecord
            rec = self.__f.read(rec_len - 5)
            if rec[-1] == Rusmarc.IS1:
                return Rusmarc(rec_len_b + rec, encoding=self.__enc)
            else:
                raise MalformedRecord
        else:
            raise StopIteration()