import redis

from app.common import logger

'''

文档地址：https://github.com/andymccurdy/redis-py

host='localhost', port=6379,
                 db=0, password=None, socket_timeout=None,
                 socket_connect_timeout=None,
                 socket_keepalive=None, socket_keepalive_options=None,
                 connection_pool=None, unix_socket_path=None,
                 encoding='utf-8', encoding_errors='strict',
                 charset=None, errors=None,
                 decode_responses=False, retry_on_timeout=False,
                 ssl=False, ssl_keyfile=None, ssl_certfile=None,
                 ssl_cert_reqs=None, ssl_ca_certs=None,
                 

redisDao = RedisDao('192.168.2.230', 6407, 'xdnphb_2016', '4')
python_version = redisDao.getRedis().get("python_version")

'''

# r = redis.StrictRedis(
#     host='192.168.2.230',
#     port='6407',
#     db='2',
#     password='xdnphb_2016',
# )


"""
    注意：
        A、redis连接实例是线程安全的，可以直接将redis连接实例设置为一个全局变量，直接使用
        B、redis实例用完，不需要手动关闭连接，底层会自动将实例放到连接池，供下次使用
"""


class RedisDao:
    # reids_conf = {
    #     'host': '192.168.2.230',
    #     'port': 6407,
    #     'db': 2,
    #     'password': 'xdnphb_2016'
    # }

    def __init__(self, host, port, db, password):
        # __pool = redis.ConnectionPool(host='192.168.2.230', port=6407, db=2, password='xdnphb_2016')
        __pool = redis.ConnectionPool(host=host, port=int(port), db=int(db), password=password, decode_responses=True)
        self.__redis = redis.Redis(connection_pool=__pool)

    def getRedis(self):
        return self.__redis

    def redis(self, call):

        try:
            return call(self.__redis)
        except Exception as e:
            logger.error(str(e.args))

        return None

    def execute(self, call):

        with self.__redis.pipeline() as pipe:
            # 开启事物
            pipe.multi()
            # 执行事物操作
            result = call(pipe)
            # 提交事物
            pipe.execute()
        return result
