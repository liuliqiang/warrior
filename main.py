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
        api.parse(XMLObject(xml_str=req_data))

        rst = api.proc_req()

        if rst.get("status", True):
            template_name = "xmlrpc/{}.jinja".format(rst.get("method_name"))
            self.render(template_name, **(rst.get("data")))
        else:
            self.write(rst.get("msg"))


application = Application([
    (r"/xmlrpc", XmlRpcHandler),
], template_path="templates")


if __name__ == "__main__":
    port = 8880
    application.listen(port)
    logger.info("Server listen at: {}".format(port))
    tornado.ioloop.IOLoop.instance().start()
