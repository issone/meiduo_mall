from celery import Celery

celery_app = Celery('meiduo')

# 加载配置文件
celery_app.config_from_object('celery_tasks.config')

# 自动注册异步任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])
