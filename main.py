#!/usr/bin/env python
# encoding: utf-8
import tornado.ioloop
import tornado.web

from utils.xmlparser import XMLObject
from services.xmlrpc import MetaWeblogApi


api = MetaWeblogApi()


class TypeException(Exception):
    def __init__(self, *args, **kwargs):
        super(TypeException, self).__init__(*args, **kwargs)


class XmlRpcHandler(tornado.web.RequestHandler):
    def post(self):
        req_data = self.request.body
        print(req_data)
        api.parse(XMLObject(xml_str=req_data))

        rst = api.invoke()

        if rst.get("status", True):
            template_name = "xmlrpc/{}.jinja".format(rst.get("method_name"))
            print(rst.get("data"))
            self.render(template_name, **(rst.get("data")))
        else:
            self.write(rst.get("msg"))

application = tornado.web.Application([
    (r"/xmlrpc", XmlRpcHandler),
], template_path="templates")


if __name__ == "__main__":
    application.listen(8880)
    tornado.ioloop.IOLoop.instance().start()
