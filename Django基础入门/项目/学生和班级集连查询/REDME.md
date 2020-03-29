本项目学生的核心功能就是实现了学生和班级列表的集合查询以及删除添加等功能

基于django1.11.11和python3.6.5开发

- 使用手册
  - 先把项目中的settings.py文件中database的数据修改成你自己的数据库链接
  - 迁移数据
    - python manage.py makemigrations
    - python manage.py migrate
  - 启动项目
    - python manage.py runserver