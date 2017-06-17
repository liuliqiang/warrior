#!/usr/bin/env python

"""
    Async database operator
    Created by yetship at 2017/6/15 下午20:52
"""
import MySQLdb
from DBUtils.PooledDB import PooledDB
from tornado import ioloop, gen
from tornado.web import asynchronous

from utils import logger


pool = PooledDB(MySQLdb, 20, host="localhost", user="root", password="password",
                db="mdpress", port=3306, charset="utf8")


def exec_sql(sql):
    conn = pool.connection()
    cur = conn.cursor()
    cur.execute(sql)
    rst = cur.fetchall
    conn.commit()
    cur.close()
    conn.close()

    return rst


def query_sql(sql):
    conn = pool.connection()
    cur = conn.cursor()
    cur.execute(sql)
    rst = cur.fetchall()
    cur.close()
    conn.close()
    return rst