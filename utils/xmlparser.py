#!/usr/bin/env python
# encoding: utf-8
from xml.etree import ElementTree as ET


class TypeException(Exception):
    def __init__(self, *args, **kwargs):
        super(TypeException, self).__init__(*args, **kwargs)


class XMLObject(object):
    def __init__(self, root=None, xml_str=None):
        if xml_str is not None:
            self.root = ET.fromstring(xml_str)
        else:
            self.root = root

    def __str__(self):
        if self.root is None:
            return ""
        elif isinstance(self.root, type([])):
            return self.root[0].text or ""
        else:
            return self.root.text or ""

    def __repr__(self):
        return self.__str__()

    def __getattr__(self, attr):
        if self.root is None:
            return XMLObject(None)
        elif isinstance(self.root, type([])):
            root_ = self.root[0]
        else:
            root_ = self.root

        name_nodes = root_.findall(attr)
        if name_nodes:
            return XMLObject(name_nodes)
        else:
            return XMLObject(None)

    # array like feature
    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return XMLObject([self.root[i] for i in range(idx.start or 0, idx.stop, idx.step or 1)])
        return XMLObject(self.root[idx])

    def __len__(self):
        if isinstance(self.root, type([])):
            return len(self.root)
        raise TypeError("object of type '{}' has no len()".format(self.__class__))

    def __iter__(self):
        if self.root is not None:
            for elem in self.root:
                yield XMLObject(elem)
            raise StopIteration
        raise TypeError("'{}' object is not iterable".format(self.__class__))


if __name__ == "__main__":
    xml_str = ""
    o2 = XMLObject(ET.fromstring(xml_str))
    print("02.__dict__ is: {}".format(o2.__dict__))
    print("o2.methodName is: {}".format(o2.methodName))
    print("o2.methodCall.methodName is: {}".format(o2.methodCall.methodName))
    print("o2.len: {}".format(len(o2.params)))
    for param in o2.params:
        print("2 param is: {}".format(param))
        print("2 param.value.root is: {}".format(param.value.root))
        print("2 param.value.root value is: {}".format(param.value.root.text))
        print("2 param.value.string is: {}".format(param.value.string))
        # print("2 param.value.string value is: {}".format(param.value.string.root.text))
