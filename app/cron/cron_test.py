from . import Scheduled
from app import logger
from app import sync

from app.sync import test_mysql as testMysql


@Scheduled(cron='0/10 * * * * ?')
# # @Scheduled(cron='0/10 * * * * ?')
# # @Scheduled(fixedRate=10)
def sync_article():
    global bquery_sql
    logger.info("==========check文章状态===========")
    testMysql.query_data()
#
# @Scheduled(cron='* 0/10 * * * ?')
# # # @Scheduled(cron='0/10 * * * * ?')
# # # @Scheduled(fixedRate=10)
# def sync_article():
#     global bquery_sql
#     logger.info("==========check文章状态===========")
#     # sync.query_data()