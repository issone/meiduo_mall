import logging
from random import randint

from rest_framework.views import APIView
from rest_framework import status
from django_redis import get_redis_connection
from rest_framework.response import Response

from meiduo_mall.apps.verifications import constants
from meiduo_mall.libs.yuntongxun.sms import CCP

logger = logging.getLogger('django')


# Create your views here.

class SMSCodeView(APIView):
    """短信验证码"""

    def get(self, request, mobile):
        redis_conn = get_redis_connection("verify_codes")
        # 判断当前手机号，60秒是否已发送过验证码
        send_flag = redis_conn.get(f"send_flag_{mobile}")
        if send_flag:
            return Response({"message": "手机号频繁发送短信"}, status=status.HTTP_400_BAD_REQUEST)

        # 生成验证码
        sms_code = '%06d' % randint(0, 999999)
        logger.info(sms_code)

        # 创建redis管道（将多次redis操作装入管道，将来一次性去执行，减少redis连接操作）
        pl = redis_conn.pipeline()
        # 把验证码存储到redis数据库
        pl.setex(f'sms_{mobile}', constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 标记手机号发送过短信
        pl.setex(f'send_flag_{mobile}', constants.SEND_SMS_CODE_INTERVAL, 1)
        # 执行管道
        pl.execute()

        # 利用容联云通讯发送短信验证码
        CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], 1)
        return Response({'message': 'ok'})
