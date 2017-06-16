#!/usr/bin/env python

"""
    A simple python script template.
    Created by yetship at 2017/6/16 下午11:58
"""
from tornado import gen


from utils import logger
from services.db import pool, exec_sql


def new_post(**post):
    # @todo: id 随机
    logger.debug("create a null post now")
    logger.debug("create a null post now")
    conn = pool.connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO post(title) VALUES ('post')")
    cur.execute("SELECT LAST_INSERT_ID()")
    post_id = cur.fetchall()[0][0]
    conn.commit()
    cur.close()
    conn.close()
    print("new post post_id: {}".format(post_id))

    post["post_id"] = post_id
    update_post(**post)

    return post_id


def update_post(**post):
    update_sql = """
        UPDATE post SET status = '{post_status}' ,
                    type = '{post_type}',
                    title = '{title}',
                    content = '{description}',
                    created_at = '{dateCreated}',
                    slug='{wp_slug}'
        WHERE id = {post_id}
    """.format(**post)

    exec_sql(update_sql)