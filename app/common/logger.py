import os

import logbook
from logbook import Logger, TimedRotatingFileHandler
from logbook.more import ColorizedStderrHandler

"""
    如何使用：
        A、run_log：表示打印在控制台
        B、日志默认打印到当前运行目录
    
        from PyTest.common.logger import run_log as logger
        logger.info("=====1======")

"""


def __log_type(record, handler):
    # print(type(record))
    # pprint(vars(logbook.base.LogRecord))
    # pprint(record.__dict__)
    # print(os.path.split(os.path.abspath(__file__))[0])

    log = "{date}  {level} {thread} --- [{thread_name}] {filename}.[{func_name}]  : {lineno} {msg}".format(
        date=record.time.strftime('%Y-%m-%d %H:%M:%S'),  # 日志时间
        level=record.level_name,  # 日志等级
        thread=record.thread,  # 日志等级
        thread_name=record.thread_name,  # 日志等级
        filename=os.path.split(record.filename)[-1],  # 文件名
        # filename=record.filename,  # 文件名
        func_name=record.func_name,  # 函数名
        lineno=record.lineno,  # 行号
        msg=record.message  # 日志内容
    )

    return log


# 日志存放路径
LOG_DIR = os.path.join('Log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 日志打印到屏幕
log_std = ColorizedStderrHandler(bubble=True)
log_std.formatter = __log_type

# 日志打印到文件
log_file = TimedRotatingFileHandler(os.path.join(LOG_DIR, '%s.log' % 'log'),
                                    date_format='%Y-%m-%d',
                                    bubble=True,
                                    encoding='utf-8')
log_file.formatter = __log_type

# 脚本日志
run_log = Logger('script_log')


def init_logger():
    logbook.set_datetime_format("local")
    run_log.handlers = []
    run_log.handlers.append(log_file)
    run_log.handlers.append(log_std)


# 实例化，默认调用
init_logger()
