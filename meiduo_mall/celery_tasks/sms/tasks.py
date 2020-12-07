from celery_tasks.sms import constants
from celery_tasks.sms.yuntongxun.sms import CCP
from celery_tasks.main import celery_app

import logging

logger = logging.getLogger('django')


@celery_app.task(name="send_sms_code")
def send_sms_code(mobile, sms_code):
    """
    发送短信的celery异步任务
    :param mobile: 手机号
    :param sms_code: 验证码
    """
    # 利用容联云通讯发送短信验证码
    try:
        CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], 1)
    except Exception as e:
        logger.error(e)
