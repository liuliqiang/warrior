#!/usr/bin/env python

"""
    A simple python script template.
    Created by yetship at 2017/6/16 下午11:58
"""
from dateutil.parser import parse

from utils import logger
from configs import conf
from services.db import pool, exec_sql, query_sql


def _build_post_url(post_id):
    return "{}/posts/{}".format(conf.BLOG_URL, post_id)


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


def get_post(post_id):
    select_sql = """SELECT created_at, content, title, slug, id FROM post WHERE id = {}""".format(post_id)

    post = query_sql(select_sql)[0]

    post = {"dateCreated": post[0].isoformat(),
            "description": post[1],
            "title": post[2],
            "post_url": _build_post_url(post_id),
            "post_id": post[4],
            "mt_keywords": "",
            "wp_slug": post[3]
    }
    return post