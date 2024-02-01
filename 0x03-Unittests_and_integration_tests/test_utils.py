#!/usr/bin/env python3
"""test utils unit"""
import unittest
from unittest.mock import patch
import requests
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized, parameterized_class


class TestAccessNestedMap(unittest.TestCase):
    """test access nested map """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested, path, result):
        """function access nested map"""
        self.assertEqual(access_nested_map(nested, pathp), result)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested, path):
        """ exception access nested map"""
        with self.assertRaises(KeyError) as error:
            access_nested_map(nested, path)

        self.assertEqual(
            f'KeyError({str(error.exception)})', repr(error.exception))


class TestGetJson(unittest.TestCase):
    """ test get json """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, testurl, testpay):
        """ test json"""
        with patch('requests.get') as mock_reque:
            mock_reque.return_value.json.return_value = testpay
            self.assertEqual(get_json(url=testurl), testpay)


class TestMemoize(unittest.TestCase):
    """test memorize test """

    def test_memoize(self):
        """test memorize"""
        class TestClass:
            """class test"""

            def a_method(self):
                """method self"""
                return 42

            @memoize
            def a_property(self):
                """property"""
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_om:
            test_class = TestClass()
            test_class.a_property()
            test_class.a_property()
            mock_om.assert_called_once()
