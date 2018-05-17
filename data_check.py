# coding=utf-8
DICT_TYPE = 1
LIST_TYPE = 2
NUMBER_TYPE = 3
STRING_TYPE = 4


def _get_type_str(data_type):
    type_str = ""
    if data_type == DICT_TYPE:
        type_str = 'dict'
    elif data_type == LIST_TYPE:
        type_str = 'list'
    elif data_type == NUMBER_TYPE:
        type_str = 'number'
    elif data_type == STRING_TYPE:
        type_str = 'str'
    else:
        raise 'err'

    return type_str


def _get_type(data):
    if isinstance(data, dict):
        return DICT_TYPE
    if isinstance(data, list):
        return LIST_TYPE
    if isinstance(data, (int, float)):
        return NUMBER_TYPE
    if isinstance(data, basestring):
        return STRING_TYPE


class DataTypeErr(Exception):
    def __init__(self, data_type, expect_type, data):
        err = "data type is {data_type} but expect type is {expect_type}".format(data_type=data_type, expect_type=expect_type)
        err += " the err value is {data}".format(data=data)
        Exception.__init__(self, err)


class KeyLostErr(Exception):
    def __init__(self, lost_key, data):
        err = "{key} is lost , keys of data is {keys}".format(key=lost_key, keys=data.keys())
        Exception.__init__(self, err)


class Term(object):
    def __init__(self, data, name=None):
        self.data_type = _get_type(data)
        self.name = name
        self.children = []
        self.analyse_data(data)

    def analyse_data(self, data):
        if self.data_type == LIST_TYPE:
            if len(data) == 0:
                raise 'err'
            term = Term(data[0])
            self.children.append(term)

        if self.data_type == DICT_TYPE:
            for key, value in data.items():
                self.children.append(Term(value, key))

    def check_data(self, data):
        # 如果当前数据类型是字典, children 存储的必然是各个key value对信息
        if self.data_type == DICT_TYPE:
            if not isinstance(data, dict):
                raise DataTypeErr(type(data), _get_type_str(self.data_type), data)
            # todo 检查是不是多了一些key
            # 检查key
            for child in self.children:
                self.check_dict_child(child, data)

        # 当前数据类型是list children 当前版本只会存储一个term, list里面所有的数据都要符合term
        if self.data_type == LIST_TYPE:
            term = self.children[0]
            for item in data:
                self.check_list_child(term, item)

    def check_list_child(self, term, data):
        # 判断类型是否正确
        if _get_type(data) != term.data_type:
            raise DataTypeErr(type(data), _get_type_str(term.data_type), data)

        # 如果类型是dict 或者list
        if _get_type(data) in (DICT_TYPE, LIST_TYPE):
            term.check_data(data)

    def check_dict_child(self, term, data):
        # 检查key是否存在
        if term.name not in data:
            raise KeyLostErr(term.name, data)

        value = data[term.name]
        # 判断value 的类型是否正确
        if _get_type(value) != term.data_type:
            raise DataTypeErr(type(value), _get_type_str(term.data_type), value)
        # 如果value的类型是dict 或者list
        if _get_type(value) in (DICT_TYPE, LIST_TYPE):
            term.check_data(value)


class Data_Check(object):
    def __init__(self, data):
        self.term = Term(data)

    def check_data(self, data):
        self.term.check_data(data)


def test_1():
    data = {"age": {"age": 10, 'data': [{"data": {"key1": 323, 'key2':323}}, {"data": {"key1": 323, 'key2':323}}]}}
    dc = Data_Check(data)
    check_data = {"age": {"age": 10, 'data': [{"data": {"key1": 323, 'key3':323}}, {"data": {"key1": 323, 'key2':323}}]}}

    dc.check_data(check_data)

if __name__ == '__main__':
    test_1()
