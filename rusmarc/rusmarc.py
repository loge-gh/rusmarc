IS3 = '\x1F'  # Begin of subfield
IS2 = '\x1E'  # End of field
IS1 = '\x1D'  # End of record


class MalformedRecord(Exception):
    pass


class Rusmarc(object):
    def __init__(self, bytestr=None, encoding='utf-8'):
        self.fields = {}
        self.status = 'n'       # default = new record
        self.type = 'a'         # default = text (excl. manuscripts)
        self.bib_level = 'm'    # default = monograph
        self.hier_level = '#'   # default = not defined
        self.control = ' '      # default = not defined
        self.coding_level = '1' # default = sublevel 1
        self.isbd = ' '         # default = record conforms ISBD rules
        if bytestr:
            self.deserialize(bytestr)

    def deserialize(self, bytestr, encoding='utf-8'):
        header = bytestr[:24]
        try:
            data_start = int(header[12:17])
        except ValueError:
            raise MalformedRecord()
        self.status = bytestr[5]
        self.type = bytestr[6]
        self.bib_level = bytestr[7]
        self.hier_level = bytestr[8]
        self.control = bytestr[9]
        self.coding_level = bytestr[17]
        self.isbd = bytestr[18]
        dictionary = bytestr[24:data_start]
        data = bytestr[data_start:]
        self.__validate(header, dictionary, data)
        self.__get_raw_fields(dictionary, data, encoding)
        self.__parse_raw_fields()

    @staticmethod
    def __validate(header, dictionary, data):
        try:
            int(header[:5])
        except ValueError:
            raise MalformedRecord()
        if header[20:] != '450 ' or header[10:12] != '22' \
                or data[-1:] != IS1 or dictionary[-1:] != IS2:
            raise MalformedRecord()

    def __get_raw_fields(self, dictionary, data, encoding):
        i = 0
        dl = len(dictionary)
        while i < dl - 1:
            try:
                fno = int(dictionary[i:i+3])
                flen = int(dictionary[i+4:i+7])
                fstart = int(dictionary[i+8:i+12])
                fval = data[fstart:fstart+flen]
                self.add_field(fno, fval.decode(encoding))
                i += 12
            except ValueError:
                raise MalformedRecord()

    def __parse_raw_fields(self):
        for fno, fval_list in self.fields.iteritems():
            parsed_val_lst = []
            for fval in fval_list:
                if fval[-1:] != IS2:
                    raise MalformedRecord()
                parsed_val_lst.append(self.__parse_raw_field(fno, fval[:-1]))
            self.fields[fno] = parsed_val_lst

    def __parse_raw_field(self, fno, fval):
        if fno >= 10:
            val = {'i1': fval[0], 'i2': fval[1], 'sf': self.__parse_raw_subfields(fval[2:])}
        else:
            val = fval
        return val

    def __parse_raw_subfields(self, sfval):
        if sfval[1] == '1':
            sfields = self.__parse_emb_fields(sfval)
        else:
            sfields = {}
            sfield_list = sfval.split(IS3)[1:]
            for sf in sfield_list:
                sfname = sf[0]
                sfval = sf[1:]
                if sfname in sfields:
                    sfields[sfname].append(sfval)
                else:
                    sfields[sfname] = [sfval]
        return sfields

    def __parse_emb_fields(self, fval):
        field_list = fval.split(IS3 + '1')[1:]
        val = {1: {}}
        for field in field_list:
            try:
                fno = int(field[0:3])
            except ValueError:
                raise MalformedRecord()
            fval = self.__parse_raw_field(fno, field[3:])
            if fno in val[1]:
                val[1][fno].append(fval)
            else:
                val[1][fno] = [fval]
        return val

    def add_field(self, fno, fval):
        if fno in self.fields:
            self.fields[fno].append(fval)
        else:
            self.fields[fno] = [fval]

    def serialize(self, encoding='utf-8'):
        dic = []
        data = []
        start = 0
        for fno, fval in self.fields:
            packed_fld = self.__pack_field(fno, fval).encode(encoding)
            l = len(packed_fld)
            dic.append("%03d%04d%05d" % (fno, l, start))
            data.append(packed_fld)
            start += l
        dic.append(IS2)
        data.append(IS1)
        dic = "".join(dic)
        data = "".join(data)
        header = "".join(("%05d" % 24 + len(dic) + len(data),
                          self.status, self.type, self.bib_level, self.hier_level,
                          self.control, '22', "%05d" % 24 + len(dic),
                          self.coding_level, self.isbd, ' 450 '))
        return "".join(header, dic, data)

    def __pack_field(self, fno, fval):
        val_list = []
        for f in fval:
            if fno >= 100:
                val = "".join((f['i1'], f['i2'], self.__pack_subfields(f['sf']), IS2))
            else:
                val = f + IS2
            val_list.append(val)
        return "".join(val_list)

    def __pack_subfields(self, sf_dic):
        res = []
        for sfn, sfv in sorted(sf_dic):
            if sfn == '1':
                res.append(self.__pack_emb_field(sfv))
                continue
            for item in sfv:
                res.append("".join((IS3, sfn, item)))
        return "".join(res)

    def __pack_emb_field(self, ef_dic):
        raise NotImplementedError()


