# 初识restFul

## 什么是REST

- 一种软件架构风格，设置风格，而不是标准，只是提供了医嘱设计原则和约束条件。它主要用于客户端和服务器交互类的软件，给予这个风格设计的软件可以更加简洁，更有层次，更易于实现缓存机制等。

## 类视图(拔高点)

### 视图函数
  
- FBV
  
  - Function Base View(基于函数的视图)

- CBV

  - Class Base View(基于类的视图)

  - 代码实例：

  - ```python
    Class HelloQiao(Views):
        #这里的get表示这个方法专门响应get请求
        def get(self,request):
            return HttpResponse("Get hehe")
        #这里的post表示这个方法专门响应post请求
        def post(self,request):
            return HttpResponse("Post hehe")
        #和相面的一样
        def put(self,request):...
        def delete(self,request):...
        def push(self,request):...
    ```

    - 在路由中配置

    `url(r"^hello/",views.HelloQiao.as_view(),name="hello")`

- 类视图
  - CBV
  - 继承自View
  - 注册的时候使用的as_view()
  - 入口
    - 不可以使用请求方法的名字作为参数名
    - 只能接受已经存在的方法
      - 定义了一个View
        - 创建了一个类视图
        - 保留，拷贝传递进来属性和参数
        - 调用dispatch方法
          - 分发
          - 如果请求方法在允许的列表中，就会找到对应的属性
          - 从自己这个对象中获取请求方法的小写对应的属性，如果没有找到，会给一个默认的没找到的默认值方法！  `http_method_not_allowed`
          - 如果请求方法不在列表里面，直接就http_method_not_allowed
