# 对于使用HyperLinkModelSerializer使用的时候需要非常注意的一个点

## 情景在线

```python

class AddressAPIView(viewsets.ModelViewSet):
    #开头四行实现了基本的设置信息
    serializer_class = AddressSerializer
    queryset = AddressModel.objects.all()
    authentication_classes = (MyAuthentication,)
    permission_classes = (MyPermission,)

    #这块为了实现对数据的修改而实现了这个create方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        user = request.user
        a_id = serializer.data.get("id")
        try:
            address = AddressModel.objects.get(pk=a_id)
            address.a_user = user
            address.save()
            print("尝试中.....")
            #请注意这一行，我希望吧自己address这个对象转换成json数据，使用了下面的代码，这里可以看源代码理解
            address_data = AddressSerializer(instance=address,context={"request":request})
            return Response(address_data.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            raise e
```

- 上面代码的解释以及原因

```python

你得到这个错误的HyperlinkedIdentityField期望接收request的context串行化的，因此它可以建立绝对的URL。在命令行上初始化序列化程序时，您无权访问请求，因此会收到错误消息。

如果需要在命令行上检查序列化程序，则需要执行以下操作：

from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from .models import Person
from .serializers import PersonSerializer

factory = APIRequestFactory()
request = factory.get('/')


serializer_context = {
    'request': Request(request),
}

p = Person.objects.first()
s = PersonSerializer(instance=p, context=serializer_context)

print s.data
您的url字段看起来像http://testserver/person/1/。
```

#### 这样使用的话最大的好处就是我们级联对象的url直接就自动生成了

```json
{
    "url": "http://127.0.0.1:8000/app1/address/30/",
    "id": 30,
    "a_address": "新加坡",
    "a_user": "http://127.0.0.1:8000/app1/user/3/"
}
```

## 对于另外的url的设置

```Python
    urlpatterns = [
    url("^user/$",views.UserView.as_view()),
    url("^user/(?P<pk>\d+)/",views.UserShow.as_view(),name="usermodel-detail"),

    #这个地方需要注意，由于我继承的是viewset.viewsets这个类
    #所以需要各位注意这里，只有他们的as_view是被重写过的，因此使用方法不同与其他
    url("^address/$",views.AddressAPIView.as_view({
        "post":"create"
    })),
    #这里的post指的是请求方法，值代表了我们调用的方法，由于viewsets继承自多个APIView，因此这些方法都是存在的！剩下的自己死磕源代码即可！
    url("^address/(?P<pk>\d+)/$",views.AddressAPIView.as_view({
        "get":"retrieve"
    }),name="addressmodel-detail")
]
```

## 级联相关的数据操作

－　需求分析：假设我们定义了一个用户和收货的值的表，每个用户可以有多个收货地址，这一点是已知的信息.我们希望用户的字段中天生包含了他所级联好的地址的相关信息该怎么做呢？

－　刚开始我的做法是这样的我使用了retrieveApiView，然后重写了retrieve方法．在方法里面获取用户的addressmodel_set数据然后在显示出来，下面是代码详细！

```python
        def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        #判断所获取到的对象的id和用户认证通过的id是否一直，从而方式某个用户的密码被破解之后直接获取其他用户的数据这种危险情况的发生！
        if instance.id != request.user.id:
            raise exceptions.PermissionDenied
        #把用户级联的地址列表数据提取出来
        address_list = [i.a_address for i in instance.addressmodel_set.all()]
        serializer = self.get_serializer(instance)
        #由于已知serializer.data是一个字典类型数据，于是直接在这改造了一下就可以了
        userdata = serializer.data
        userdata["address_list"] = address_list
        return Response(userdata)

    ＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊
    结果：
        {
            "url": "http://127.0.0.1:8000/app1/user/3/",
            "id": 3,
            "u_name": "Jack",
            "u_password": "123456",
            "address_list": [
                "新加坡",
                "香港"
            ]
        }
```

#### 但是上面的方法不是很帅

- 这里是比较好的方法！

```python
#这里是serializer.py文件中

    #由于接下来需要被引入的原因这里地址这个主表就先定义了
    class AddressSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = AddressModel
            fields = ("url","id","a_address","a_user")

    class UserSerializer(serializers.HyperlinkedModelSerializer):
        #定义了一个字段，字段名称是我们上面对象的隐性属性的名称，级联的目标是主表类名
        #传递了两个参数 many=True , read_only=True
        addressmodel_set = AddressSerializer(many=True,read_only=True)

        class Meta:
            model = UserModel
            #这里的参数列字段中需要加入上面定义好了的外键引用的隐性属性名
            fields = ("url","id","u_name","u_password","addressmodel_set")

        #强烈换衣fields字段中使用了反射的属性，只有模型带有的字段才可以显示，自己定义的就不行！我们的xxx_set其实就是一个自带的隐性属性

    ＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊
    注意：如果你非要使用一个不是原有的字段名，你就需要去修改模型！

    -models.py
    class UserModel(models.Model):

    u_name = models.CharField(max_length=32,unique=True)
    u_password = models.CharField(max_length=128)

    class AddressModel(models.Model):

    a_address = models.CharField(max_length=128,unique=True)
    a_user = models.ForeignKey(UserModel,related_name="address_list",null=True,blank=True)
    #这个地方的relate_name其实就是定义一个关联的名称，自己定义的自己用．

    之后：serializer.py

    class AddressSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = AddressModel
            fields = ("url","id","a_address","a_user")

    class UserSerializer(serializers.HyperlinkedModelSerializer):
        #这个时候还是反射，不过关联的名字就是自己定义的那个名字了
        address_list = AddressSerializer(many=True,read_only=True)

        class Meta:
            model = UserModel
            fields = ("url","id","u_name","u_password","address_list")
            #下面也一样一样的

```

- 结果

```json
{
    "url": "http://127.0.0.1:8000/app1/user/3/",
    "id": 3,
    "u_name": "Jack",
    "u_password": "123456",
    "addressmodel_set": [
        {
            "url": "http://127.0.0.1:8000/app1/address/1/",
            "id": 1,
            "a_address": "新加坡",
            "a_user": "http://127.0.0.1:8000/app1/user/3/"
        },
        {
            "url": "http://127.0.0.1:8000/app1/address/2/",
            "id": 2,
            "a_address": "香港",
            "a_user": "http://127.0.0.1:8000/app1/user/3/"
        }
    ],
    "address_list": [
        "新加坡",
        "香港"
    ]
}
```

- 可以看到上面的结果多了两行完整的数据信息！
