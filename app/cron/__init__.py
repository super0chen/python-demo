import inspect

from flask_apscheduler import APScheduler

__all__ = ['scheduled_init']

jobs = []


# 定义定时器注解
def Scheduled(**kwds):
    def decorate(f):
        global dic
        name = getattr(f, '__name__')
        class_path = inspect.stack()[1][1]
        class_name = class_path[class_path.replace('\\', '/').rfind('/') + 1:].replace('.py', '')

        if 'fixedRate' in kwds:
            fixed_rate = kwds['fixedRate']
            dic = {
                'func': 'app.cron.' + class_name + ':' + name,
                'id': name,
                'args': '',
                'trigger': 'interval',
                'seconds': int(fixed_rate),
                'replace_existing': True
            }

        elif 'cron' in kwds:
            cron = kwds['cron'].strip().replace('?', '*').split(' ')
            dic = {
                'func': 'app.cron.' + class_name + ':' + name,
                'id': name,
                'args': '',
                # 'trigger': {
                #     'type': 'cron',
                #     'second': '*/5',  # 秒
                #     'minute': '0-59',  # 分钟
                #     'hour': '0-23',  # 小时
                #     'day': '',  # 日
                #     'month': '',  # 月
                #     'day_of_week': "MON-FRI",  # 星期
                # },
                'trigger': {
                    'type': 'cron',
                    'second': cron[0],  # 秒
                    'minute': cron[1],  # 分钟
                    'hour': cron[2],  # 小时
                    'day': cron[3],  # 日
                    'month': cron[4],  # 月
                    'day_of_week': cron[5],  # 星期
                },
                'replace_existing': True
            }

        jobs.append(dic)
        return f

    return decorate


# 定时器初始化操作
def scheduled_init(app):
    scheduler = APScheduler()
    app.config['JOBS'] = jobs
    scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()


# 这个导入必须放在最后
import app.cron.cron_test
