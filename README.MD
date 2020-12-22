本项目使用python3.7, Django3.1.3版本
前后端分离，重新实现美多商城项目

坑点1：
    数据库使用mysql时，会报错，解决办法，[点击查看](https://www.cnblogs.com/huchong/p/13744417.html)

坑点2：
    drf-extensions使用redis作缓存时，会报错，解决办法
    方法1： 将django降级到3.0
    方法2： 修改drf-extensions源码，在对应的路径下
    site-packages/rest_framework_extensions/key_constructor/bits.py
    修复EmptyResultSet的引用
    将 from django.db.models.sql.datastructures import EmptyResultSet
    改为 from django.core.exceptions import EmptyResultSet 
    