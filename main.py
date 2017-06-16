#!/usr/bin/env python
# encoding: utf-8
import tornado.ioloop
from tornado import gen
from tornado.web import asynchronous, Application, RequestHandler

from utils import logger
from utils.xmlparser import XMLObject
from services.xmlrpc import MetaWeblogApi


api = MetaWeblogApi()


class TypeException(Exception):
    def __init__(self, *args, **kwargs):
        super(TypeException, self).__init__(*args, **kwargs)


class XmlRpcHandler(RequestHandler):
    @asynchronous
    @gen.engine
    def post(self):
        req_data = self.request.body
        print(req_data)
        api.parse(XMLObject(xml_str=req_data))

        rst = api.proc_req()

        if rst.get("status", True):
            template_name = "xmlrpc/{}.jinja".format(rst.get("method_name"))
            print(rst.get("data"))
            self.render(template_name, **(rst.get("data")))
        else:
            self.write(rst.get("msg"))


class TestHandler(RequestHandler):
    @asynchronous
    @gen.engine
    def get(self, *args, **kwargs):
        from datetime import datetime
        from services.db import worker
        self.write("begin at: {}<br/>".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        yield worker(1)
        logger.info("OK")
        self.write("finish at: {}<br/>".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.finish("ok")


application = Application([
    (r"/xmlrpc", XmlRpcHandler),
    (r"/test", TestHandler)
], template_path="templates")


if __name__ == "__main__":
    application.listen(8880)
    tornado.ioloop.IOLoop.instance().start()
