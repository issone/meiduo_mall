import os

from celery import Celery

# 告诉celery 如果需要使用Django的配置文件,应该去那里加载
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev")

celery_app = Celery('meiduo')

# 加载配置文件
celery_app.config_from_object('celery_tasks.config')

# 自动注册异步任务
celery_app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])
