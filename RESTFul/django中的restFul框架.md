# 重量级RESTful

- django-rest-framework

- REST难点

  - 模型序列化

    - 正向序列化

      - 将模型转换成JSON

    - 反向序列化

      - 将JSON转换成模型

  - Serializer

    - 在模块serializers

      - HyperLinkedModelSerializer
        - 序列化模型并且添加超链接
      - Serializer
        - 手动序列化

## REST-Framework

- 序列化器
  - Serializer

- 命名规范
  - 拒绝中文，空格，特殊字符，.......
  - 拒绝数字开头，拒绝￥开头
  - 小写字母或者大写字母开头，驼峰命名
  - 远离框架名称

## HelloREST

- 序列化器

- 视图函数

  - viewsets.ModelViewSet

  - CBV

  - 视图集合

- 路由
  
  - routers.DefaultRouter

- 记得在INSTALLED_APPS添加rest_framework

- runserver
  - 所以api可视化了
  - 超链接
    - HyperLinkModelSerializer
  - 对数据集合实现了
    - 路由 /users/, /groups/
    - get
    - post
  - 对单个数据实现了
    - 路由 /users/id/ , /groups/id/
    - get
    - post
    - put
    - delete
    - patch
  - viewsets做了视图函数的实现
  - router做了路由的注册