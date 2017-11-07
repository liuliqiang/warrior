#!/usr/bin/env python

"""
    A simple python script template.
    Created by yetship at 2017/6/16 下午11:58
"""
from datetime import datetime

import MySQLdb

from utils import logger
from configs import conf
from services.db import pool, exec_sql, query_sql


POST_STATUS = ('PUBLISHED', 'DELETED', 'EDITING', 'SCHEDULING')


def _build_post_url(post_id):
    return "{}/posts/{}".format(conf.BLOG_URL, post_id)


def new_post(**post):
    # @todo: id 随机
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
    post["posts_count"] = 0
    post["comments_count"] = 0
    post["created_by"] = 1
    post["published_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    post["date"] = post["published_at"]
    update_post(**post)

    return post_id


def update_post(**post):
    if post['post_status'] not in POST_STATUS:
        post['post_status'] = POST_STATUS[0]

    update_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_sql = """UPDATE post
                    SET status=%s,type=%s,title=%s,content=%s,
                    created_at=%s,published_at=%s,updated_at=%s,slug=%s,
                    posts_count=%s,created_by=%s,date=%s
                    WHERE id = %s"""

    exec_sql(update_sql,
             post['post_status'], post['post_type'], post['title'], post['description'],
             post['dateCreated'], post['published_at'], update_date, post['wp_slug'],
             post['posts_count'], post['created_by'], post['date'],
             post['post_id'])


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
