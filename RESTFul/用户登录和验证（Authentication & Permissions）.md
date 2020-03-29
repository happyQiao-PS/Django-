# 用户登录和验证（Authentication & Permissions）

- 用户注册
  - RESTFul
  - 数据开始
    - 模型，数据库
    - 创建用户
      - 用户身份
      - 普通
      - 删除用户
  - 注册实现
    - 添加了超级管理员生成
- 用户登录
  - 验证用户名和密码
  - 生成用户令牌
  - 出现了和用户注册公用的post冲突
    - 添加action
    - path?action=login
    - path?action=register
    - 捕获异常的精确
- 用户认证
  - BaseAuthentication
    - authenticate
      - 认真成功会返回一个元祖
        - 第一个元素是user
        - 第二个元素是令牌 token auth
- 用户权限
  - BasePermission
    - has_permission
      - 是否具有权限
        - True用有权限
        - False未拥有权限
- 用户认证和权限
  - 直接配置在视图函数上就ok了



