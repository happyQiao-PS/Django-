# 双R（Request & Response）

- Request
  - rest_framework
  - APIView
    - render_classes(渲染的类)
    - parser_classes(解析转换的类)
    - authentication_classes(认证的类)
    - throttle_classes(节流的类)
      - 节流的类
      - 控制请求频率的类
    - permission_classes(权限的类)
      - 控制权限
    - content_negotiation_class(内容过滤)
    - metadata_class(元信息过滤)
    - versioning_class(版本信息过滤)
    - as_view()
      - 调用父类的as_view -> dispatch
        - dispatch被重写了
        - initialize_request
          - 使用django的request构建了REST_framework中的request
          - 将django中的request构建成了自己request，并且把原来的request封装成为了_request属性
          - 属性和方法
            - content_type
            - stream
            - query_params
            - data
              - POST请求中是可以获取GET参数的
              - 比如我们把?name=xxx加入到POST请求的末尾
              - 然后在视图函数里面使用GET方法获取参数是完全OK的
              - 此方法适用于DELETE,PATCH,PUT等方法
                - user
                  - 可以直接在请求上获取用户
                  - 相当于请求上添加了一个属性罢了
            - auth
              - 认证
              - 相当于请求上添加了一个属性，属性值是token
            - successful_authxxx
            - initial
              - perform_authentication
                - 执行用户认证
                - 遍历了用户认证器
                  - 如果认证成功，返回元祖
                  - 第一个元素就是user,第2个元素就是token
              -check_permissions
                - 检察权限
                - 遍历权限认证器
                - 只要一个权限认证未通过，就直接拒绝
                - 所有权限都有才行
              - check_throttles
                - 检查频率
                - 遍历频率限制器
                  - 如果遍历不通过，就等待、
                - csrf_exempt
                  - 所有的APIView的自雷都是csrf豁免的

## Response

- 自己封装的
  - data直接接受字典转换成Json数据
  - return Response(data)
  - status 状态码
- 依然是HttpResponse的子类

- 属性和方法
  - rendered_content
  - status_text

- 对于视图函数的包装  
  - CBV
    - 直接继承自APIView
  - FBV
    - api_view()装饰器方法，可以普通的函数视图加一个装饰器让他支持类视图并且是restfulframework的APIView的方法，这样就可以非常舒服的使用各种控制的方法了
    - 装饰器需要一个参数，http_method_names=["GET","POST"]
    - 这个参数可以支持到我们http请求的各种方法，只需要加载到装饰器中就可以了

### 上面讲的很容易懵逼，接下来瞅一眼自己的源代码好了

- class StudentViewSet(ListAPIView,CreateAPIView,DestroyAPIView,UpdateAPIView):
  - queryset = Student.objects.all()
  - serializer_class = StudentSerialzer

- 上面的代码可以看到一些端倪出来，首先我直接多继承了上面的四个类，分别是增删改查四个大类，原因在是他们都同意的集成了一个父类GenericAPIView，这个类里面有英文提示告诉你，要么自己添加这两个字段，要么重写两个方法。随后会有一些方法出现，自己观察他继承的另外一个类，你会发现，这四个类的代码规范出奇的一致，都是在上一层被继承的类里面调用mixin.xxxx类里面的方法，我们会发现，使用的这四个类下一定会定义一些方法，比如你是listapiview那么在这个类里面的第一个方法一般就是get方法，这样我们就比较明确了。原来在使用get请求的时候，多继承会自动调用到listapvie中的get方法，同样如果是post方法的话，就会自动调用createapiview类里面的post方法，以此类推destroyapiview也就会自动调用delete方法，put或者patch方法就会自动调动updateapiview中的put方法，如果你看懂了这里说明你已经很牛逼了，这里看懂了之后，接下来的难度就会降下来很多，有可能自己就可以才出来接下来了，由于这四个类均集成了genericapiview这个类，再加上这个类里面的主要参数是完全相同的所以我们这需要传递这两个参数就可以一下子吧这么多问题全部解决了
- 这里需要注意的是
- 如果传递put或者post请求的时候，我们需要在路由器里面修改代码增加一个命名空间为pk，这里是当我们需要获取某一个元素的时候需要传递一个id个后台使用的，他的代码在这4个类里面并没有明确的体现，但是在最底层的继承类View中我们发现纯在相关的kwargs的操作，可能是他们的问题
- 使用get方法的时候不要图简单使用浏览器来直接查询，会报错告诉你没有相关的模板，但是数据其实已经到达前端了，只是没有被渲染出来罢了，建议使用pycharm的http测试工具，或者httpie,postman等请求的专属的测试工具来测试，在实际使用的时候，建议前后端分离！让前段node.js，Vue,Jquery等来渲染数据即可。
