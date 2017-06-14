#!/usr/bin/env python
# encoding: utf-8
from xml.etree import ElementTree as ET

import tornado.ioloop
import tornado.web
import xmltodict


class TypeException(Exception):
    def __init__(self, *args, **kwargs):
        super(TypeException, self).__init__(*args, **kwargs)


class ReqObject(object):
    def __init__(self, dict_):
        self.dict_ = dict_

    def __str__(self):
        if not self.dict_:
            return ""

        if not isinstance(self.dict_, type("")):
            raise TypeException("not a node value")
        return str(self.dict_)

    def __getattr__(self, attr):
        if attr in self.dict_:
            return ReqObject(self.dict_[attr])
        else:
            return ReqObject({})

    # array like feature
    def __getitem__(self, idx):
        return ReqObject(self.dict_[idx])

    def __len__(self):
        return len(self.dict_)

    def __iter__(self):
        for elem in self.dict_:
            yield ReqObject(elem)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        req_data = self.request.body
        print(req_data)
        obj = ReqObject(xmltodict.parse(req_data))
        print(obj.dict_)
        print(obj.__dict__)
        print(obj.methodCall.methodName)
        print(len(obj.methodCall.params.param))
        for param in obj.methodCall.params.param:
            print(param.value.string)
        # tree = ET.fromstring(req_data)

        # method_name_nodes = tree.findall("methodName")
        # if not method_name_nodes:
        #     return False
        # method_name = method_name_nodes[0].text
        # if method_name != "blogger.getUsersBlogs":
        #     return False

        # params_root_nodes = tree.findall("params")
        # if not params_root_nodes:
        #     return False
        # params_nodes = params_root_nodes[0].getchildren()
        # if not params_nodes or len(params_nodes) != 3:
        #     return False
        # appkey, username, password = [param_node.findall("value")[0].findall("string")[0].text for param_node in params_nodes]

        self.write("")


application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8880)
    tornado.ioloop.IOLoop.instance().start()
    # obj = ReqObject({"a": "b", "c": {"d": "e"}})
    # print(str(obj.test))
    # print(obj.a)
    # print(obj.c)
    # print(obj.c.d)
