#!/usr/bin/env python
# encoding: utf-8
import tornado.ioloop
import tornado.web

from utils.xmlparser import XMLObject


class TypeException(Exception):
    def __init__(self, *args, **kwargs):
        super(TypeException, self).__init__(*args, **kwargs)


class XmlRpcHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        req_data = self.request.body
        print(req_data)
        obj = XMLObject(xml_str=req_data)
        # for param in obj.params:
        #     print(param.value.string)

        method_name = obj.methodName
        print("method_name: {}".format(method_name))
        # if method_name != "blogger.getUsersBlogs":
        #     self.write("no support method")

        appkey, username, password = [param.value.string for param in obj.params]
        print('appkey: {}'.format(appkey))
        print('username: {}'.format(username))
        print('password: {}'.format(password))

        self.render("xmlrpc/getUsersBlogs.jinja",
                    blog_name="Tornado 测试博客",
                    xmlrpc_url="http://localhost:8880/xmlrpc",
                    is_admin="true",
                    blog_id="0000000001",
                    blog_url="http://localhost:8880")


application = tornado.web.Application([
    (r"/xmlrpc", XmlRpcHandler),
], template_path="templates")


if __name__ == "__main__":
    application.listen(8880)
    tornado.ioloop.IOLoop.instance().start()
