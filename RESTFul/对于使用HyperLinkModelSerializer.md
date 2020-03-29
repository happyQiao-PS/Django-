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