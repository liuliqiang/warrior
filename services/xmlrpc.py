#!/usr/bin/env python

"""
    A simple python script template.
    Created by yetship at 2017/6/14 下午11:22
"""
from tornado import gen
from dateutil.parser import parse

from utils import logger
from configs import conf

from services import (auth as auth_srv,
                      category as ctg_srv,
                      media as media_srv,
                      post as post_srv)


class MetaWeblogApi(object):
    def __init__(self, req_obj=None):
        if req_obj is not None:
            self.req_obj = req_obj

    def parse(self, req_obj):
        self.req_obj = req_obj

    def invoke(self):
        print(self.req_obj.methodName)
        api_version, method_name = str(self.req_obj.methodName).split(".")

        rst = {"data": self.__getattribute__("_" + method_name)(),
               "api_version": api_version,
               "method_name": method_name}

        return rst

    def proc_req(self):
        return self._check_auth() and self.invoke()

    def _check_auth(self):
        _, username, password = [p.value.string for p in self.req_obj.params.param[:3]]
        return auth_srv.check(username, password)

    def _getUsersBlogs(self):
        """
        Returns information about all the blogs a given user is a member of.
        """
        return {
            "blog_name": conf.BLOG_NAME,
            "xmlrpc_url": "{}/xmlrpc".format(conf.BLOG_URL),
            "is_admin": "true",
            "blog_id": "0000000001",
            "blog_url": conf.BLOG_URL
        }

    def _getPost(self):
        post_id = self.req_obj.params.param[0].value.string

        post = post_srv.get_post(post_id)

        return post

    def _newPost(self):
        post = {
            "post_status": self.req_obj.params.param[3].value.struct.member[0].value.string,
            "post_type": self.req_obj.params.param[3].value.struct.member[1].value.string,
            "categories": [category.data.value.string for category in self.req_obj.params.param[3].value.struct.member[2].value.array],
            "title": self.req_obj.params.param[3].value.struct.member[3].value.string,
            "dateCreated": parse(self.req_obj.params.param[3].value.struct.member[4].value.root[0].findall("dateTime.iso8601")[0].text).strftime("%Y-%m-%d %H:%M:%S"),
            "wp_slug": self.req_obj.params.param[3].value.struct.member[5].value.string,
            "description": self.req_obj.params.param[3].value.struct.member[6].value.string,
            "mt_keywords": self.req_obj.params.param[3].value.struct.member[7].value.string,
            "oper": self.req_obj.params.param[4].value.boolean,
        }

        result = post_srv.new_post(**post)
        print("result: {}".format(result))
        return {"post_id": result}

    def _editPost(self, req_obj):
        return {}

    def _deletePost(self, req_obj):
        return {}

    def _getCategories(self):
        """
        Retrieve list of categories.
        """
        return {"categories": ctg_srv.get_categories()}

    def _newMediaObject(self):
        blog_id = str(self.req_obj.params.param[0].value.string)
        filename = str(self.req_obj.params.param[3].value.struct.member[2].value.string)
        mime_type = str(self.req_obj.params.param[3].value.struct.member[3].value.string)
        bits = str(self.req_obj.params.param[3].value.struct.member[1].value.base64)
        overwrite = str(self.req_obj.params.param[3].value.struct.member[0].value.boolean)

        image_url = media_srv.save_image(filename, bits)
        return {"media_url": image_url}

    def _getTemplate(self, req_obj):
        return {}

    def _setTemplate(self, req_obj):
        return {}


if __name__ == "__main__":
    mb = MetaWeblogApi()
    mb.invoke()