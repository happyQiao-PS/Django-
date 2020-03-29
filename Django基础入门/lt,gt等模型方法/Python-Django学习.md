---
typora-copy-images-to: pic
---

# Python-Django学习

filter和exclude是Django的if/else

filter()表示匹配满足要求的数据，而exclude()则表示匹配不满足要求的数据。

需要注意的是filter()括号里面有很多的匹配选项

这里只需要在pycharm里面打入需要判断的字符变量,然后就可以看到很多的末尾带有

#### LT / GT

先来说一下lt-->less than, gt-->great than

其实就是大于和等于，注意有几个是末尾带有eq 的那个才是大于等于或者小于等与！

代码实例：

```python
def input(request):
    for i in range(1,15):
        student = Student()
        flag = random.randint(0,100)
        student.s_name = "Tony"+str(flag)+random.choice("abcdefghijklmnopqrstuvwxyz")
        student.s_age = flag
        student.s_sex = random.choice([0,1])
        student.save()
    return HttpResponse("data input scuess !")


def show(request):
    students = Student.objects.filter()
    context = {
        "students":students,
    }
    return render(request,"showDemo.html",context=context)


def delete(request):
    students = Student.objects.filter(s_sex=1)
    students.delete()
    students = Student.objects.filter()
    return render(request,"showDemo.html",context={"students":students})
```

这些代码里面可以看到我们日常最长见的判断代码的实例！很有用的！



# 2 . 创建对象的方式

1.直接创建对象

```python
def input(request)：
    student = Student()
    flag = random.randint(0,100)
    student.s_name = "Tony"+str(flag)+random.choice("abcdefghijklmnopqrstuvwxyz")
    student.s_age = flag
    student.s_sex = random.choice([0,1])
    student.save()
    return HttpResponse("data input scuess !")
```

2.利用方法创建对象

```python
def create_student(request):
    student = Student.objects.create(s_name="Qiao",s_age=22,s_sex=True)
    student.save()
```

前者看上去会更容易理解一些，但是后者确实更加简单了.但是呢！第2种方法需要格外注意的是如果有字段没有赋值那么数据库里的数据将不会被设置为默认值，也就是说每一个字段都需要赋值才行！

注意我们也可以直接Student(s_name="xxx",s_age=xxx,s_sex="xx").但是这里的问题和上面的是一样的，必须全部赋值好，不然就会有问题。并且绝对不可以尝试重写

```python
__init__.py
```

来解决这个问题



### 方法

--对象方法

​				-可以调用对象的属性，也可以调用类的属性

--类的方法

​				-不能调用对象属性，只能调用类的属性

--静态方法

​				-啥都不可以调用，不能获取对象属性

​				-只是寄生在这个类里面罢了！



#### 原因：我们正常的创建对象的习惯是建一个类，然后直接创建对象也就是下面的代码

```python
class Class1:
	def __init__(self,name,age):
			self.name = name
			self.age = age
if __name__ == "__main__":
	class1 = Class1(name="xxx",age=xxx)#这里就是创建对象的方法了
```

在Django中我们建立了models的模型类，然后我们也可以像面向对象使用完全一样的方法来创建这样的一个对象。但是上面已经讲过了，如果直接创建的话，如果我们没有传入默认值，那么代码将会把它设置成空，`并且我们也不可以使用重写`init方法来解决这个问题，这个其实算是一个bug了。那么接下来的方法就是如何解决这个问题的了！

#### 解决方案

```python

# Create your models here.
class Student(models.Model):
    s_name = models.CharField(max_length=20,db_column="name",unique=True)
    s_age = models.IntegerField(db_column="age")
    s_sex = models.BooleanField(max_length=2,db_column="sex")

    @classmethod
    def create_people(cls,name,age=100,sex=True):#这里创建了一个类方法
        return cls(s_name=name,s_age=age,s_sex=sex)#这里返回了一个类对象

    class Meta:
        db_table = "Student"
```

```python
def create_student(request):
    student = Student.create_people("Qiaomo")#这里直接调用就可以了
    student.save()
    return HttpResponse("OK")
```

那么类里面的cls又是什么东西呢？

接下来的代码好好看看！

```python
class A(object):
    a = 'a'
    @staticmethod
    def foo1(name):
        print 'hello', name
        print A.a # 正常
        print A.foo2('mamq') # 报错: unbound method foo2() must be called with A instance as first argument (got str instance instead)
    def foo2(self, name):
        print 'hello', name
    @classmethod
    def foo3(cls, name):
        print 'hello', name
        print A.a
        print cls().foo2(name)
```

> > @staticmethod和@classmethod都可以直接类名.方法名()来调用，那他们有什么区别呢
> >  从它们的使用上来看,
> >  @staticmethod不需要表示自身对象的self和自身类的cls参数，就跟使用函数一样。
> >  @classmethod也不需要self参数，但第一个参数需要是表示自身类的cls参数。
> >  如果在@staticmethod中要调用到这个类的一些属性方法，只能直接类名.属性名或类名.方法名。
> >  而@classmethod因为持有cls参数，可以来调用类的属性，类的方法，实例化对象等，避免硬编码。
>
> 也就是说在classmethod中可以调用类中定义的其他方法类的属性，但staticmethod只能通过A.a调用类的属性，但无法通过在该函数内部调用A.foo2()。修改上面的代码加以说明：



#### 所以我们可以看到如果吧上面的代码修改成如下的代码：

```python
class Student(models.Model):
    s_name = models.CharField(max_length=20,db_column="name",unique=True)
    s_age = models.IntegerField(db_column="age")
    s_sex = models.BooleanField(max_length=2,db_column="sex")

    @classmethod
    def create_people(cls,name,age=100,sex=True):
        cls_1 = cls()
        cls_1.s_name = name
        cls_1.s_age = age
        cls_1.s_sex = sex
        return cls_1
        # return cls(s_name=name,s_age=age,s_sex=sex)

    class Meta:
        db_table = "Student"
```

代码的运行结果是完全相同的，我们可以看到cls就是代表了这个类自己，所以cls(里面添加的变量)其实就是赋值说需要的操作罢了！

#### ##这样我们在联想一下前面的学习就知道，由于django的原因我们无法直接调用Student的init方法，但是我们却可以使用类方法的特性：调用Student 类的默认init方法，然后为其传值！



# 排序

### order by

django这个排序和mysql的order by类似！我们可以先使用[类名.objects.all().orderby()]来实现排序，需要注意的是:

---1.不加order by默认是按照id进行排序的。

---2.order by里面是一个字符串，没有代码提示的需要注意。

---3.虽然没有提示，但是可以告诉你，就是你在models里面定义的字段名。

---4.如果想要升序排序，直接filter就可以了，但如果要降序排序需要加一个"-"。

#### 下面是演示Demo

```python
def show(request):
    students = Student.objects.filter().order_by("-s_age")
    context = {
        "students":students,
    }
    return render(request,"showDemo.html",context=context)
```

![2020-02-01 17-41-26屏幕截图](/home/qiao/图片/2020-02-01 17-41-26屏幕截图.png)

# values

### 如果我们需要调试数据或者吧数据转换为json的话可以使用这个属性！

[类名.objects.values]

可以拿到一个QuerySet的数据，里面有一个大列表数据，列表内部嵌套好了很多字典，每一个字典就是一个对象！这样的数据可以比较方便转换成为json数据库文件

```python
def show(request):
    students = Student.objects.filter().order_by("-s_age")
    student_value = students.values()
    for student_val in student_value:
        print(student_val)
    context = {
        "students":students,
    }
    return render(request,"showDemo.html",context=context)
```

返回结果:

```json
{'s_name': 'Qiaomo', 'id': 1, 's_sex': True, 's_age': 100}
{'s_name': 'Tony98h', 'id': 8, 's_sex': False, 's_age': 98}
{'s_name': 'Tony90n', 'id': 10, 's_sex': True, 's_age': 90}
{'s_name': 'Tony80c', 'id': 9, 's_sex': True, 's_age': 80}
{'s_name': 'Tony73b', 'id': 11, 's_sex': True, 's_age': 73}
{'s_name': 'Tony71e', 'id': 3, 's_sex': True, 's_age': 71}
{'s_name': 'Tony63k', 'id': 5, 's_sex': True, 's_age': 63}
{'s_name': 'Tony57x', 'id': 13, 's_sex': False, 's_age': 57}
{'s_name': 'Tony54a', 'id': 7, 's_sex': False, 's_age': 54}
{'s_name': 'Tony53a', 'id': 12, 's_sex': True, 's_age': 53}
{'s_name': 'Tony48t', 'id': 14, 's_sex': True, 's_age': 48}
{'s_name': 'Tony35i', 'id': 2, 's_sex': True, 's_age': 35}
{'s_name': 'Tony24i', 'id': 4, 's_sex': False, 's_age': 24}
{'s_name': 'Tony22p', 'id': 6, 's_sex': True, 's_age': 22}
{'s_name': 'Tony2t', 'id': 15, 's_sex': True, 's_age': 2}
```

# 其他的方法：

first/last 

objects.all().first()/objects.all().last()

--默认 是没有上面问题的

--隐藏bug

​		-可能会出现first和last完全相同的对象（有可能！）

​				--手动写排序算法吧！

exists

object.exists==>True/False

![2020-02-01 17-56-11屏幕截图](/home/qiao/文档/pic/2020-02-01 17-56-11屏幕截图.png)



# 网络服务器的报错提示：

## 5xx的错误都是服务器崩溃了！这个很尴尬的！

### 其他:

#### 2xx:请求是成功了

#### 3xx:被转发了

#### 4xx:客户端挂了



# get的毛病

--1.如果尝试get一个不存在的数据那么我们的程序会抛出一个500异常，

--2.如果查询对象存在多个值的时候，他还是会抛出异常，并且异常的原因就是返回的数据超过一个了！



# 切片

--和python不太一样

--QuerySet[5:15]     #获取第五条到第十五条数据

​		-相当于SQL语句中的limit和offset

​		-不需要优化算法了，直接就可以在数据库里面限制好要查询的数据了

​		-注意这里的切片大多数都是左闭右开的区间



# 缓存集

--filter

--exclude

--all

--都不会真正的查询数据库

--只有在迭代结果集或者获取单个对象属性的时候才会查询数据库

--懒查询   

# 查询条件

- 属性__运算符=值

- gt
- lt
- gte
- lte
- in在某一集合中
- contains 类似于 模糊查询like
- startswith 以xx开始  本质也是like
- endswith 以xx结束 也是like
- exact 精确查询
- 前面添加i,忽略大小写的匹配
  - iall
  - iget
  - istartswith
  - iendswith
  - icontains
  - .......
-  django中查询条件有时区问题
  - 关闭Django中的自定义时区#setting -->USE_TZ=False即可
  - 在数据库中创建对应的时区表

- 