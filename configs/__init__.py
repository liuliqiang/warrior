#!/usr/bin/env python

"""
    Config base class for operate config args.
    Created by yetship at 2017/6/14 下午11:40
"""
#!/usr/bin/env python
# encoding: utf-8
import os
import logging


class Config(object):
    def __init__(self):
        env = os.environ.get("AIRFLOW_CONFIG_ENVIROMENT", "LOCAL")
        if env.upper() == "PRODUCTION":
            from configs.prod import DataSourceProdConfig
            self._config = DataSourceProdConfig
        elif env.upper() == "TEST":
            from configs.test import DataSourceTestConfig
            self._config = DataSourceTestConfig
        else:
            from configs.local import DataSourceLocalConfig
            self._config = DataSourceLocalConfig

    def __getattr__(self, item):
        """
        1. get config value from python files
        2. if config not in python file, read from enviroments for secret value
        """
        value = self._config.__dict__.get(item, None)
        if not value:
            return os.environ.get(item.upper())

    # default config following

    # project config following
    PROJECT_NAME = "Warrior"
    LOGGING_FORMAT = "[%(asctime)s  %(filename)-24s:%(lineno)4s] %(message)s"
    LOGGING_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"
    LOGGING_LEVEL = logging.DEBUG

    # blog config
    BLOG_NAME = "Tornado 测试博客"
    BLOG_URL = "http://localhost:8880"
    BLOG_ID = ""

    TMP_PATH = "/tmp"

conf = Config()
