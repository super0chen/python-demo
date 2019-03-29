import json
import ujson

import requests
import arrow

from app import baseDao
from app import logger

# 文档：http://note.youdao.com/noteshare?id=c0243b89787a80f7638a3bdb77a60fd2&sub=6B3CCC5B479F4D73B62332F8E518ABE8

# json转换工具：https://www.json.cn/

__SELECT_SQL = """
    SELECT * FROM sys_user where id < 100
    """


def query_data():
    # 查询多条数据
    datas = baseDao.query_sql(__SELECT_SQL)
    logger.info(ujson.dumps(datas))

    return ""
