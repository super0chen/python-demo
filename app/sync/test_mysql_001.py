import json
import ujson

import requests
import arrow

from app.common.BaseDao import BaseDao
from app import logger

# 文档：http://note.youdao.com/noteshare?id=c0243b89787a80f7638a3bdb77a60fd2&sub=6B3CCC5B479F4D73B62332F8E518ABE8

# json转换工具：https://www.json.cn/


baseDao = BaseDao("192.168.2.210", "3306", "phb_data", "xdnphb", "xdnphb_2015")

__SELECT_SQL = """
    SELECT * FROM sys_user where id < 100
    """

__SELECT_SQL_PARAMS = """
    SELECT * FROM sys_user where id < %s
    """


# 查询数据
def query_data():
    # 查询多条数据
    datas = baseDao.query_sql(__SELECT_SQL)
    logger.info(ujson.dumps(datas))

    # 传参查询
    datas = baseDao.query_sql(__SELECT_SQL_PARAMS, ["100"])
    logger.info(ujson.dumps(datas))

    # 传参查询，只取一条数据
    data = baseDao.query_sql(__SELECT_SQL_PARAMS, ["100"], first=True)
    logger.info(ujson.dumps(data))

    # count数据条数
    count = baseDao.query_count_sql(__SELECT_SQL_PARAMS, ["100"])
    logger.info(count)


# 新增数据
def insert_data():
    count = baseDao.insert_sql("insert into test_python(name, age) values(%s, %s)", ["tomA", "20"])
    logger.info(count)

    count = baseDao.insert("test_python", {"name": "tomB", "age": "22"})
    logger.info(count)


# 更新数据
def update_data():
    # > -1 表示更新成功
    count = baseDao.update_sql("update test_python set name=%s where id=%s", ["updateA", "1"])
    logger.info(count)

    count = baseDao.update("test_python", {"name": "tom3", "age": "23"}, "id=%s", ["3"])
    logger.info(count)


# 事务操作
def exec_data():
    # > -1 表示更新成功

    def call(cur):
        baseDao.execute_sql(cur, "update test_python set name=%s where id=%s", ["test_exec1", "1"])
        baseDao.execute_sql(cur, "update test_python set name=%s where id=%s", ["test_exec2", "2"])
        baseDao.execute_sql(cur, "update test_python set name=%s where id=%s", ["test_exec3", "3"])

    baseDao.execute(call)


if __name__ == '__main__':
    # query_data()
    # insert_data()
    # update_data()
    exec_data()
