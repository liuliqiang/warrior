#!/usr/bin/env python

"""
    Service for media operation
    Created by yetship at 2017/6/15 上午2:08
"""
import os
import base64

from configs import conf


def save_image(filename, b64data):
    file_path = os.path.join(conf.TMP_PATH, filename)
    with open(file_path, "wb") as fh:
        fh.write(base64.decodebytes(bytes(b64data, encoding="utf-8")))