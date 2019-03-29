import re
import pymysql
import attr
import datetime
from datetime import datetime
from datetime import date
from app.common import logger
from DBUtils.PersistentDB import PersistentDB

'''
host='192.168.2.210',
port='',
user='xdnphb',
password='xdnphb_2015',
db='phb_data',
charset='utf8mb4',
'''

"""
    使用方法:
       
         baseDao = BaseDao('localhost', '3306', 'dream', 'dream', 'dreamcd123456')
        
        
        # 查询
    
        # mymysql自身做了防止sql注入
        # sql = 'select * from sys_user where id=%s'
        # datas = baseDao.queryOne(sql, ('1'))
    
        # insert
        sql = 'insert into test(name1, age) value(%s, %s)'
        # sql = 'insert into test(id, name, age) value(99,%s, %s)'
        datas = baseDao.insert_id(sql, ['g', '1'])
    
        print(datas)
        print(type(datas))
        
"""


class BaseDao:
    __host = []

    def __init__(self, host, port, database, username, password, charset=None):

        self.__pool = self.__pool_mysql(host, port, database, username, password, charset)

    def query_sql(self, sql: str, params=None, first=False) -> list:
        """

        :param sql: sql语句
        :param params: where条件的值：如: ['1', '2']
        :param first: 是否查询单条数据
        :return: None：表示异常，否则：first 为 True 或 False: 分别返回 {}, []
        """

        try:
            return self.__query(1, None, sql, None, params, first, None, None)
        except Exception as err:
            logger.error('异常：%s ' % str(err))

        return None

    def query_count_sql(self, sql: str, params=None) -> int:
        """根据条件查询匹配的count数

        :param sql:
        :param params: where条件的值：如: ['1', '2']
        :return: -1：表示异常，>-1: 表示正常
        """
        try:
            return self.__query(3, None, sql, None, params, True, None, None)
        except Exception as err:
            logger.error('异常：%s ' % str(err))

        return -1

    def insert_sql(self, sql: str, params: list):
        """

        :param sql:
        :param params: where条件的值：如: ['1', '2']
        :return: -1：表示异常，>-1：表示当前插入数据的自增ID值
        """

        try:
            return self.__execute_sql(0, sql, params)
        except Exception as err:
            logger.error('异常：%s ' % str(err))

        return -1

    def update_sql(self, sql: str, params: list):
        """

        :param sql:
        :param params: where条件的值：如: ['1', '2']
        :return: -1：表示异常，>-1: 表示正常
        """

        try:
            return self.__execute_sql(1, sql, params)
        except Exception as err:
            logger.error('异常：%s ' % str(err))

        return -1

    def delete_sql(self, sql: str, params: list):
        """

        :param sql:
        :param params: where条件的值：如: ['1', '2']
        :return: -1：表示异常，>-1: 表示正常
        """

        try:
            return self.__execute_sql(2, sql, params)
        except Exception as err:
            logger.error('异常：%s ' % str(err))

        return -1

    def query(self, table: str, columns: list, where=None, params=None, first=False, order_by=None, limit=None) -> list:
        """

        :param table:
        :param columns:
        :param where: 'name=%s and age=10'
        :param params: where条件的值：如: ['1', '2']
        :param first: 是否查询单条数据
        :param order_by: age desc, name asc，该条件小心sql注入
        :param limit: 0,20
        :return: None: 表示异常，否则： first为true或False: 分别返回 {}, []
        """

        try:
            return self.__query(2, columns, table, where, params, first, order_by, limit)
        except Exception as err:
            logger.error('异常：%s ' % str(err))

        return None

    def insert(self, table: str, data: object) -> int:
        """

        :param table: sys_user
        :param data: {'name': 'tom', age: '10'}
        :return: -1：表示异常，>-1：表示当前插入数据的自增ID值
        """

        try:
            return self.__cud(None, 0, table, None, data)
        except Exception as err:
            logger.error('异常：%s ' % str(err))

        return -1

    def update(self, table: str, sets: dict, where=None, params=None) -> int:
        """

        :param table:
        :param sets: {'name': 'tom', age: '10'}
        :param where: 'name=%s and age=10'
        :param params: where条件的值：如: ['1', '2']
        :return: -1：表示异常，>-1：表示正常
        """

        try:
            return self.__cud(None, 1, table, sets, where, params)
        except Exception as err:
            logger.error('异常：%s ' % str(err))

        return -1

    def delete(self, table: str, where=None, params=None) -> int:
        """

        :param table:
        :param where: 'name=%s and age=10'
        :param params: where条件的值：如: ['1', '2']
        :return: -1：表示异常，>-1：表示正常
        """

        try:
            return self.__cud(None, 2, table, None, where, params)
        except Exception as err:
            logger.error('异常：%s ' % str(err))

        return -1

    def insert_conn(self, cur, table: str, data: object) -> int:
        """

        :param cur: 事务游标
        :param table:
        :param data: {'name': 'tom', age: '10'}
        :return:
        """

        return self.__cud(cur, 0, table, None, data)

    def update_conn(self, cur, table: str, sets: dict, where=None, params=None) -> int:
        """

        :param cur: 事务游标
        :param table:
        :param sets: {'name': 'tom', age: '10'}
        :param where: 'name=%s and age=10'
        :param params: where条件的值：如: ['1', '2']
        :return:
        """

        return self.__cud(cur, 1, table, sets, where, params)

    def delete_conn(self, cur, table: str, where=None, params=None) -> int:
        """

        :param cur: 事务游标
        :param table:
        :param where: 'name=%s and age=10'
        :param params: where条件的值：如: ['1', '2']
        :return:
        """
        return self.__cud(cur, 2, table, None, where, params)

    def execute_sql(self, cur, sql: str, params=None) -> None:
        """ 事物操作

        :param callback: callback的参数是cursor
        :return:
        """

        if self.__empty(params, list):
            raise ValueError('通过sql查询，params只能是list')

        if self.__empty(sql, str):
            raise ValueError('sql只能str, 且不能为空')

        cur.execute(sql, params)

    def execute(self, callback):
        """ 事物操作

        :param callback: callback的参数是cursor
        :return:
        """
        return self.__execute(0, callback)

    """
        ===============================================
        ===============================================
        ===============================================
        ==================以下是私有方法=================
        ===============================================
        ===============================================
        ===============================================
    """

    def __pool_mysql(self, host, port, database, username, password, charset=None):

        return PersistentDB(
            creator=pymysql,  # 使用的数据库模块
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始回话前要执行的命令列表
            ping=0,  # ping mysql客户端检查是否可用

            # A、False表示不关闭: conn.close()操作将被忽略,供下次使用线程关闭时,才会自动关闭链接
            # B、False表示要关闭: conn.close()则关闭链接,再次调用pool.connection时就会报错,因为已经真的关闭了连接
            # C、pool.steady_connection()可以获取一个新的链接
            closeable=False,  # 是否关闭链接
            threadlocal=None,  # 本线程独享值的对象，用于保存链接对象,如果链接被重置
            host=host,
            port=int(port),
            user=username,
            password=password,
            db=database,
            charset='utf8mb4' if charset is None else charset,
            cursorclass=pymysql.cursors.DictCursor
        )

    def __conn(self):
        return self.__pool.connection()

    def __execute(self, status: int, callback):

        """装饰方法

        :param status: 0：表示事物操作, 1:表示insert/update/delete操作, 2: 表示查询操作
        :param callback: status=0, 回调参数是connection, 否则是cursor
        :return: object
        """

        conn = None

        try:

            conn = self.__conn()
            cur = conn.cursor()

            if status == 0:
                conn.begin()

            result = callback(cur)
            conn.commit()

        except Exception as err:
            if (status < 2) and conn is not None:
                conn.rollback()
            raise err
        else:
            # 释放数据库资源
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

        return result

    def __cud(self, cur, status: int, table: str, sets: dict, data: object, params=None) -> int:

        params = self.__paramsToStr(params)

        try:

            def call(d_cur):

                sql = None
                param = None
                error_sql = ''

                # insert
                if status == 0:
                    sql, param, error_sql = self.__sql_insert(table, data)
                # update
                elif status == 1:
                    sql, param, error_sql = self.__sql_update(table, sets, data, params)
                # delete
                elif status == 2:
                    sql, param, error_sql = self.__sql_delete(table, data, params)

                try:
                    count = d_cur.execute(sql, param)

                except Exception as error:
                    raise Exception('ErrorSql: %s, %s' % (error_sql, str(error.args)))

                return 0 if count == 0 else d_cur.lastrowid

            if cur is None:
                return self.__execute(1, call)
            else:
                return call(cur)

        except Exception as err:

            raise err

    def __query(self, status: int, columns: list, sql_or_table: str, where: str, params: list, first: bool,
                order_by: str,
                limit: str):

        params = self.__paramsToStr(params)

        try:
            def call(cur):
                count = 0
                # 根据sql语句查询
                if status == 1 or status == 3:

                    if not (self.__empty(params, list) or self.__empty(params, tuple)):
                        raise ValueError('通过sql查询，params只能是list/tuple')

                    if self.__empty(sql_or_table, str):
                        raise ValueError('通过sql查询，sql只能str, 且不能为空')
                    elif not re.match('^select', sql_or_table.strip().lower()):
                        raise ValueError('通过sql查询，sql不是有效的查询语句')

                    count = cur.execute(sql_or_table, params)

                # 根据where条件查询
                elif status == 2 or status == 4:
                    sql, param, sql_error = self.__sql_query(first, sql_or_table, columns, where, params, order_by,
                                                             limit)
                    count = cur.execute(sql, param)

                if status == 1 or status == 2 or status == 3:
                    # 查询一条数据
                    if first:

                        r_data = {}
                        if count > 0:
                            d_data = cur.fetchone()
                            if status == 3:
                                r_data = 0
                                for k, v in d_data.items():
                                    r_data = int(v)
                                    break
                            else:
                                r_data = self.__do_result_data(d_data)

                        return r_data
                    # 查询多条数据
                    else:

                        r_datas = []
                        if count > 0:
                            d_list = cur.fetchall()
                            for d_data in d_list:
                                r_data = self.__do_result_data(d_data)

                                r_datas.append(r_data)

                        return r_datas
                else:
                    return count

            return self.__execute(2, call)

        except Exception as err:
            raise err

    def __sql_insert(self, table: str, data: object):

        if self.__empty(table, str):
            raise ValueError('insert: table不能为None且必须为str')

        if attr.has(data):
            data = attr.asdict(data)
        else:
            if self.__empty(data, dict):
                raise ValueError('insert: data不能为None,或必须被attr.has()识别')

        columns = []
        params = []
        values = []
        for k, v in data.items():
            if v is not None and v != 'None':
                params.append('%s')
                columns.append(self.__do_column(k))
                # if isinstance(v,)
                values.append(self.__doStr(v))

        table = self.__do_column(table)
        columns = ', '.join(columns)
        params = ', '.join(params)
        sql_values = ', '.join(values)

        sql = 'insert into {table}({columns}) values({params})'.format(table=table, columns=columns,
                                                                       params=params)
        error_sql = 'insert into {table}({columns}) values({params})'.format(table=table, columns=columns,
                                                                             params=sql_values)

        return sql, values, error_sql

    def __sql_update(self, table: str, sets: dict, where: str, params: list):

        if self.__empty(table, str):
            raise ValueError('update: table不能为None且必须为str')

        if self.__empty(sets, dict):
            raise ValueError('update: sets必须为dict')

        sql_where, where_error, set_sql, set_sql_error = self._do_where(where, params, sets)

        table = self.__do_column(table)

        sql = 'update {table} {sets} {where}'.format(table=table, sets=set_sql, where=sql_where)
        error_sql = 'update {table} {sets} {where}'.format(table=table, sets=set_sql_error, where=where_error)

        return sql, params, error_sql

    def __sql_delete(self, table: str, where: str, params: list):

        if self.__empty(table, str):
            raise ValueError('delete: table不能为None且必须为str')

        sql_where, sql_where_error, set_sql, set_sql_error = self._do_where(where, params, None)

        table = self.__do_column(table)

        sql = 'delete from {table} {where}'.format(table=table, where=sql_where)
        error_sql = 'delete from {table} {where}'.format(table=table, where=sql_where_error)

        return sql, params, error_sql

    def __sql_query(self, first: bool, table: str, columns: list, where: str, params: list, order_by: str, limit: str):

        if self.__empty(table, str):
            raise ValueError('query: table不能为None且必须为str')

        if columns is not None and not (isinstance(columns, list) or isinstance(columns, tuple)):
            raise ValueError('query: columns必须为list/tuple')

        sql_columns = '*'
        where_sql, sql_where_error, set_sql, set_sql_error = self._do_where(where, params, None)

        if self.__not_empty(columns, list):
            sql_columns = []
            for column in columns:
                sql_columns.append(self.__do_column(column))
            sql_columns = ', '.join(sql_columns)

        sql_order_by = ''
        sql_limit = ''
        if first:
            if self.__not_empty(order_by, str):
                sql_order_by = 'order by ' + order_by

            if self.__not_empty(limit, str):
                sql_limit = 'limit ' + limit

        table = self.__do_column(table)
        sql = 'select {columns} from {table} {where} {order_by} {limit}'.format(columns=sql_columns, table=table,
                                                                                where=where_sql, order_by=sql_order_by,
                                                                                limit=sql_limit)
        sql_error = 'select {columns} from {table} {where} {order_by} {limit}'.format(columns=sql_columns, table=table,
                                                                                      where=sql_where_error,
                                                                                      order_by=sql_order_by,
                                                                                      limit=sql_limit)
        return sql, params, sql_error

    def __execute_sql(self, status, sql: str, params=None):
        """事物操作

        :param params: where条件的值：如: ['1', '2']
        :param sql:
        :return:
        """

        if status == 0:
            if self.__empty(sql, str):
                raise ValueError('通过sql insert数据，sql只能str, 且不能为空')
            elif not re.match('^insert into', sql.lower()):
                raise ValueError('通过sql insert数据，sql不是有效的insert into语句')

        elif status == 1:
            if self.__empty(sql, str):
                raise ValueError('通过sql update数据，sql只能str, 且不能为空')
            elif not re.match('^update', sql.lower()):
                raise ValueError('通过sql update数据，sql不是有效的update语句')

        elif status == 2:
            if self.__empty(sql, str):
                raise ValueError('通过sql delete数据，sql只能str, 且不能为空')
            elif not re.match('^delete', sql.lower()):
                raise ValueError('通过sql delete数据，sql不是有效的delete语句')

        if not (self.__empty(params, list) or self.__empty(params, tuple)):
            raise ValueError('params只能是list/tuple')

        params = self.__paramsToStr(params)

        def callback(cur):
            count = cur.execute(sql, params)
            return 0 if count == 0 else cur.lastrowid

        return self.__execute(1, callback)

    def _do_where(self, where: str, params: list, sets=None):
        if where is None:
            where = ''
        elif not isinstance(where, str):
            raise ValueError('update: where条件必须为str')

        if params is None:
            params = []
        elif not isinstance(params, list):
            raise ValueError('update: params条件必须为list')

        d_where = []
        where_len = 0

        set_sql = ''
        set_sql_error = ''

        set_params = []

        if sets is not None and len(sets) > 0:

            d_sets = []
            d_sets_error = []

            for k, v in sets.items():
                if v == '%s':
                    v = params.pop(0)
                v = str(v)

                d_sets.append(k + '=%s')
                set_params.append(v)
                d_sets_error.append(k + '=' + v)

            set_sql = ' set ' + ', '.join(d_sets)
            set_sql_error = ' set ' + ', '.join(d_sets_error)

        if len(where) > 0:
            d_where = re.split("%s", where)
            where_len = len(d_where) - 1

            if d_where.count('') > 0:
                d_where.remove('')

            where = ' where ' + where

        if len(params) > 0 and len(params) == where_len:

            for i in range(len(params)):
                d_where[i] = d_where[i] + params[i]

            sql_where_error = ' where ' + ''.join(d_where)

        else:
            raise ValueError('query: where条件不为None并且有%s时，params不能为None')

        for i in params:
            set_params.append(i)
        params.clear()
        params.extend(set_params)

        return where, sql_where_error, set_sql, set_sql_error

    def __do_result_data(self, data):
        r_data = {}
        for d in data:

            v = data[d]
            if v is not None:

                if isinstance(v, datetime):
                    v = v.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(v, date):
                    v = v.strftime('%Y-%m-%d')
                else:
                    v = str(v)
                r_data[d] = v

        return r_data

    def __condition_sql(self):
        return ['=', '>', '>=', '<', '<=', '!=', 'LIKE', 'NOT LIKE', 'IN', 'NOT IN']

    def __do_column(self, s):
        return '`' + s + '`'

    def __not_empty(self, s, type):
        return self.__isinstance(s, type) and len(s) > 0

    def __isinstance(self, s, type):
        return s is not None and isinstance(s, type)

    def __empty(self, s, type):

        # print(s is not None)
        # print(isinstance(s, type))
        # print(len(s) > 0)
        # print(self.__not_empty(s, type))

        return not self.__not_empty(s, type)

    def __doStr(self, s):
        s = str(s)
        if s == 'True':
            s = '1'
        elif s == 'False':
            s = '0'
        return s

    def __paramsToStr(self, params):
        d_params = []
        if self.__not_empty(params, list):
            for i in range(len(params)):
                d_params.append(str(params[i]))
        return d_params


# 测试
def __test():
    """ 测试用到的表
    CREATE TABLE `sys_user` (
      `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户表',
      `name` varchar(100) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '姓名',
      `nickname` varchar(100) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '昵称',
      `intime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

    :return:
    """
    print("========1======")
    # baseDao = BaseDao('localhost', '3306', 'dream', 'dream', 'dreamcd123456')
    print("========2======")

    # r = baseDao.query_sql('select * from sys_user where name=%s and nickname=%s', ['xc10', 20])
    # r = baseDao.query('sys_user', None, 'name=%s and nickname=%s', ['a', 'a'])

    # r = baseDao.query_count_sql('select count(*) from sys_user where a=%s and b=%s', ['1', '2'])

    # r = baseDao.insert_sql('select * from sys_user where name=%s and nickname=%s', ['xc10', 20])
    # r = baseDao.insert('sys_user', {'name': 'xc10', 'nickname': '20'})

    # r = baseDao.update('sys_user', {'name': '%s', 'nickname': '22'}, 'a=%s and b=%s', ['100', '1', '2'])
    # def delete(self, table: str, where: str, params: list) -> int:

    # r = baseDao.delete('sys_user', 'a=%s and b=%s', ['1', '2'])

    print("========3======")
    # print(r)
    print("========4======")

    # def call(cur):
    #
    #     baseDao.update_conn(cur, 'test', {'name': 'ss'}, [('id', '=', '2')])
    #     cur.execute('update test set name1=%s where id=%s', ['ff', '1'])
    #     # cur.execute('update test set name1=%s where id=%s', ['aaaa9', '8'])
    #
    #     return 1
    #
    # try:
    #     datas = baseDao.execute(call)
    #     logger.info(datas)
    # except Exception as e:
    #     logger.info(e.args)

# __test()
