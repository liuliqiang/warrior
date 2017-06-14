#!/usr/bin/env python

"""
    Service for category operation
    Created by yetship at 2017/6/15 上午1:02
"""
from configs import conf


def get_categories():
    return [{
        "html_url": "{}/catalog/336753".format(conf.BLOG_URL),
        "desc": "default",
        "title": "default",
        "id": "3367534",
        "rss_url": ""
    }]