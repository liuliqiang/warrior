#!/usr/bin/env python

"""
    Production config for project
    Created by yetship at 2017/6/14 下午11:43
"""
from . import Config


class DataSourceProdConfig(Config):
    def __init__(self):
        super(DataSourceProdConfig, self).__init__()