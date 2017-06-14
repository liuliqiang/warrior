#!/usr/bin/env python

"""
    A simple python script template.
    Created by yetship at 2017/6/14 下午11:22
"""
from utils import logger
from configs import conf

from services import (auth as auth_srv)


class MetaWeblogApi(object):
    def __init__(self, req_obj):
        self.req_obj = req_obj

    def invoke(self):
        api_version, method_name = str(self.req_obj.methodName).split(".")

        rst = self.__getattribute__("_" + method_name)()

        rst["api_version"] = api_version
        rst["method_name"] = method_name

        return rst

    def proc_req(self):
        return self._check_auth() and self.invoke()

    def _check_auth(self):
        _, username, password = [p.value.string for p in self.req_obj.params]
        return auth_srv.check(username, password)

    def _getUsersBlogs(self):
        return {
            "blog_name": conf.BLOG_NAME,
            "xmlrpc_url": "{}/xmlrpc".format(conf.BLOG_URL),
            "is_admin": "true",
            "blog_id": "0000000001",
            "blog_url": conf.BLOG_URL
        }

    def _getPost(self, req_obj):
        return {}

    def _newPost(self, req_obj):
        return {}

    def _editPost(self, req_obj):
        return {}

    def _deletePost(self, req_obj):
        return {}

    def _getCategories(self, req_obj):
        return {}

    def _newMediaObject(self, req_obj):
        return {}

    def _getTemplate(self, req_obj):
        return {}

    def _setTemplate(self, req_obj):
        return {}


if __name__ == "__main__":
    mb = MetaWeblogApi()
    mb.invoke()