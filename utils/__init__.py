#!/usr/bin/env python

"""
A simple python script template.
Created by yetship at 2017/6/14 下午11:37
"""
import logging

from configs import conf


logger = logging.getLogger(conf.PROJECT_NAME)
logging.basicConfig(format=conf.LOGGING_FORMAT)
logger.setLevel(conf.LOGGING_LEVEL)