import os
import yaml

from app.common.BaseDao import BaseDao

from app.common import logger
from settings.config import AppConfig

__all__ = ["init", "logger", "baseDao", "env_status", "is_dev", "is_test", "is_product"]

baseDao = BaseDao

env_status = ''
is_dev = False
is_test = False
is_product = False


class Config(object):
    JOBS = []
    SCHEDULER_API_ENABLED = True


def import_env():
    if os.path.exists('.env'):
        print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            key, value = var[0].strip(), var[1].strip()
            os.environ[key] = value


# 初始化定时器
def initConfig():
    env = os.getenv("ENVSTATUS")
    if env is None:
        env = 'dev'
        import_env()

    global env_status, is_dev, is_test, is_product

    env_status = env

    is_dev = env == 'dev'
    is_test = env == 'test'
    is_product = env == 'product'

    AppConfig.env = env_status
    AppConfig.is_dev = is_dev
    AppConfig.is_test = is_test
    AppConfig.is_product = is_product

    current_path = os.path.abspath(os.path.dirname(__file__))
    current_path = current_path.replace("\\", "/").replace('/app', '/settings') + '/config.yml'
    with open(current_path, 'r') as f:
        em = yaml.load(f.read())
        conf = em[env]

    dices = {}
    for key in conf:
        dices.update(conf[key])

    for field in dir(AppConfig):
        if not callable(field) and not field.startswith("__"):
            val = dices.get(field)
            if val is not None:
                setattr(AppConfig, field, val)


def init(app):
    initConfig()

    global baseDao
    # 初始化数据库
    baseDao = BaseDao(AppConfig.dbHost, AppConfig.dbPort, AppConfig.dbDatabase, AppConfig.dbUsername,
                      AppConfig.dbPassword)

    app.debug = False
    app.secret_key = '6,BmA9zoLfBzLLr)xP)1l@xm9s@8O7V('

    from app.cron import scheduled_init
    scheduled_init(app)

    # 下面这些form 必须要在上的变量初始化之后才能导入，如果放在baseDao初始化之前导入，会报错ImportError: cannot import name 'baseDao'
    from app.restful import test

    app.register_blueprint(test, url_prefix='/test')
