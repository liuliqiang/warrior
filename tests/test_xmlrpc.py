#!/usr/bin/env python

"""
    MetaWeblogApi test
    Created by yetship at 2017/6/14 下午11:53
"""
import unittest
from collections import OrderedDict

from services.xmlrpc import MetaWeblogApi
from utils.xmlparser import XMLObject


class TestMetaWeblogAPI(unittest.TestCase):
    def setUp(self):
        self.mwa = MetaWeblogApi()

    def test_invoke(self):
        with open("data/inputs/001.xml", "r") as f:
            data = f.read()
        self.mwa.parse(XMLObject(xml_str=data))
        self.rst = self.mwa.invoke()
        real_rst = "&".join(["{}={}".format(k, v) for k, v in sorted(self._format_data().items())])

        with open("data/outputs/001.txt", "r") as f:
            expected_rst = f.read()
        self.assertEqual(expected_rst, real_rst)

    def test_getUsersBlogs(self):
        with open("data/inputs/001.xml", "r") as f:
            data = f.read()
        self.mwa.parse(XMLObject(xml_str=data))
        self.rst = self.mwa.invoke()
        real_rst = "&".join(["{}={}".format(k, v) for k, v in sorted(self._format_data().items())])

        with open("data/outputs/001.txt", "r") as f:
            expected_rst = f.read()
        self.assertEqual(expected_rst, real_rst)

    def test_getCategories(self):
        with open("data/inputs/002.xml", "r") as f:
            data = f.read()
        self.mwa.parse(XMLObject(xml_str=data))
        self.rst = self.mwa.invoke()
        self.assertEqual(len(self.rst["data"]["categories"]), 1, "Categories count error")

        print(self.rst["data"])
        self.rst["data"] = self.rst["data"]["categories"][0]
        real_rst = "&".join(["{}={}".format(k, v) for k, v in sorted(self._format_data().items())])

        with open("data/outputs/002.txt", "r") as f:
            expected_rst = f.read()
        print(real_rst)
        self.assertEqual(expected_rst, real_rst, "getCategories rst format error")

    def _format_data(self):
        self.rst["data"] = "&".join(["{}={}".format(k, v) for k, v in sorted(self.rst["data"].items())])
        return self.rst