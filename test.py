# coding=utf-8
import unittest
from data_check import *


class TestDataCheck(unittest.TestCase):
    def test_data_type_err_1(self):
        """
        测试type err
        :return:
        """
        data = {"age": {"age": 10, 'name': 'llili'}}
        dc = Data_Check(data)
        check_data = {"age": {"age": '323', 'name': 'llili'}}
        self.assertRaises(DataTypeErr, dc.check_data, check_data)

        check_data = {"age": {"age": 343, 'name': 434.545}}
        self.assertRaises(DataTypeErr, dc.check_data, check_data)

        check_data = {"age": {"age": [], 'name': 434.545}}
        self.assertRaises(DataTypeErr, dc.check_data, check_data)

    def test_data_type_err2(self):
        """
        测试 list 内部的检查
        :return:
        """
        data = {"age": {"age": 10, 'data': [{"age": 11}, {'age': 2}]}}
        dc = Data_Check(data)
        check_data = {"age": {"age": 10, 'data': [{"age": 11}, {'age': '343'}]}}
        self.assertRaises(DataTypeErr, dc.check_data, check_data)

        check_data = {"age": {"age": 10, 'data': [{"age": 11}, [13]]}}
        self.assertRaises(DataTypeErr, dc.check_data, check_data)

    def test_data_type_err3(self):
        data = {"age": {"age": 10, 'data': [{"data": {"key1": 323, 'key2':323}}, {"data": {"key1": 323, 'key2':323}}]}}
        dc = Data_Check(data)
        check_data = {"age": {"age": 10, 'data': [{"data": {"key1": 323, 'key2':{'date': 'err'}}}, {"data": {"key1": 323, 'key2':323}}]}}
        self.assertRaises(DataTypeErr, dc.check_data, check_data)

    def test_data_key_lost_1(self):
        data = {"age": {"age": 10, 'data': [{"data": {"key1": 323, 'key2':323}}, {"data": {"key1": 323, 'key2':323}}]}}
        dc = Data_Check(data)
        check_data = {"age": {"23": 10, 'data': [{"data": {"key1": 323, 'key2':323}}, {"data": {"key1": 323, 'key2':323}}]}}
        self.assertRaises(KeyLostErr, dc.check_data, check_data)

        check_data = {"age": {"age": 10, 'data': [{"data": {"key1": 323, 'key3':323}}, {"data": {"key1": 323, 'key2':323}}]}}
        self.assertRaises(KeyLostErr, dc.check_data, check_data)


if __name__ == '__main__':
    unittest.main()