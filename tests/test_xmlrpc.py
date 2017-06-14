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
    def test_invoke(self):
        with open("data/inputs/001.xml", "r") as f:
            data = f.read()
        mwa = MetaWeblogApi(XMLObject(xml_str=data))
        rst = mwa.invoke()
        real_rst = "&".join(["{}={}".format(k, v) for k, v in sorted(rst.items())])

        with open("data/outputs/001.txt", "r") as f:
            expected_rst = f.read()
        self.assertEqual(expected_rst, real_rst)

    def test_getUsersBlogs(self):
        with open("data/inputs/001.xml", "r") as f:
            data = f.read()
        mwa = MetaWeblogApi(XMLObject(xml_str=data))
        rst = mwa.invoke()
        real_rst = "&".join(["{}={}".format(k, v) for k, v in sorted(rst.items())])

        with open("data/outputs/001.txt", "r") as f:
            expected_rst = f.read()
        self.assertEqual(expected_rst, real_rst)

