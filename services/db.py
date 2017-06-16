#!/usr/bin/env python

"""
    Async database operator
    Created by yetship at 2017/6/15 下午20:52
"""
from tornado import ioloop, gen
from tornado.web import asynchronous
from tornado_mysql import pools

from utils import logger


pools.DEBUG = True


POOL = pools.Pool(dict(host='127.0.0.1', port=3306, user='root',
                       passwd='password', db='mdpress'),
                  max_open_connections=100,
                  max_recycle_sec=3)


@gen.coroutine
def create_null_post():
    logger.debug("create a null post now")
    tran = yield POOL.begin()
    yield tran.execute("INSERT INTO post(title) VALUES ('post')")
    cur = yield tran.execute("SELECT LAST_INSERT_ID()")
    yield tran.commit()
    print(cur.fetchall())


@gen.coroutine
def exec_sql(sql, n):
    logger.info("worker: {} sleeping {} seconds".format(n, 1))
    cur = yield POOL.execute(sql, ())
    logger.info("worker: {} fetchall: {}".format(n, cur.fetchall()))


@gen.coroutine
def worker(n):
    executors = [exec_sql("SELECT SLEEP({})".format(3), i) for i in range(1)]
    yield executors


@gen.coroutine
def main():
    # workers = [worker(i) for i in range(10)]
    # yield workers
    yield create_null_post()


if __name__ == "__main__":
    ioloop.IOLoop.current().run_sync(main)
    logger.info(POOL._opened_conns)