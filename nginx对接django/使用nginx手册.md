# Nginx配置文件

## Nginx常用指令

- 常用的启动指令

```sql
    nginx
    #这个命令可以直接启动你的nginx服务器
```

- 信息查看
  - nginx   -v 查看版泵好
  - nginx   -V  查看安装以及调试的信息

## Nginx控制

- nginx -s **signal**

```linux
    stop [直接退出]
    quit [优雅的退出]
    reload [重新载入]
```

## 通用的linux系统管理方式

``` linux
    service nginx start
    service nginx stop
    service nginx status
    service nginx enable
    service nginx disable
```

**不建议这样关闭，因为系统强制关闭会导致部分配置文件丢失***

## 配置常用

- Negix配置文件包含指定控制的模块

  - 制定分为简单指令和块指令

  - 一个简单指令由名称和参数组成，以空格分割，并且以分号结束

  - 一个块指令和简单指令具有相同的结构，但不是以分号结束，而是以一个大括号包围了一堆附加指令结束，有点类似json
    数据格式。

  - 如果一个大括号可以由其他的指令，他就称为一个上下文，比如(events,http,server,location)

- 指令
  - nginx -t              不运行，经测试配置文件
  - nginx -c configpath   从指定路径加载配置文件
  - nginx -t -c configpath 测试制定的配置文件（最好使用绝对路径）

-Nginx配置文件结构

```linux
    main    全局设置

    events{     工作模式，连接配置
        ...
    }
    http{       http的配置
        ...
        upstream  xxx{      负载均衡配置
            ...
        }
        server{         主机设置
            ...
            location xxx{       URL匹配
                ...
            }
        }

    }
```

- linux中var目录通常喜欢存放一些越使用就会越来越大的文件

## events

- 指定工作模式以及链接上限

```linux

    events{
        use epoll;
        worder_connections:1024;
    }

```

- use指定nginx工作模式

  - epoll     高效工作模式（Linux）

  - kqueue    高效工作模式,(bsd)

  - poll      标准模式

  - select    标准模式

- worker_connections:定义nginx的每一个进程的最大连接数
  
  - 正向代理    连接数*进程数

  - 方向代理    链接数*进程数/4

  - linux系统限制最多能同事打开65535个文件，默认上限就是65535，可以接触ulimit -n 65535

## http

- 最核心的模块，主要负责http服务器相关配置，包含server,upstream子模块

  - include mime.types;   设置文件的mime类型

  - include xxxconfig;    包含其他配置文件，分开规划解码

  - default_type  xxx;    设置默认类型为二进制流，文件类型未知时会使用默认

  - log_format      设置日志的格式

  - sendfile        设置高效文件传输模式

  - keepalive_timeout   设置客户端连接活跃超时

  - gzip             gzip压缩，可以提升运行效率

## Server

- 用来指定虚拟主机

  - listen 80;      指定虚拟主机监听的端口
  
  - server_name:localhost;  指定ip地址或域名，多个域名使用空格隔开

  - charset utf-8;    指定网页的默认编码格式

  - error_page 500 502/50x.html     指定错误页面

  - access_log  xxx.main;指定虚拟主机的访问日志

  - error_log  xxx.main; 指定虚拟主机的错误日志的存放路径

  - root  xxx;  指定这个虚拟主机的根目录

  - index xxx;  指定默认首页

## location

- 核心中的核心，以后的主要配置都在这

- 主要的功能定位url,解析url，支持正则匹配，还能支持条件，实现动静分离

- 语法

```linux
    location [modefier] url{
        ...
    }
```

- modefier 修饰符

  - =  使用精确匹配并且终止搜索

  - ～ 区分大小写的正则表达式

  - ～* 不区分大小写的正则表达式

  - ^~ 最佳匹配，不是正则匹配，通常用来匹配目录

- 常用指令

  - alias  别名，定义location的其他名字，在文件系统中能够找到，如果location指定了正则表达式将会引用正则表达式中的捕获，alias替代了location中匹配的部分，没有匹配的部分将会在文件系统中搜索。

## 使用uwsgi服务器为Django进行反向解析对接

- 首先需要安装uwsgi反向解析服务器
  
  - `pip install uwsgi`

- uwsgi常规配置方案
  
  - >其实百度上面有很多类似的文件，你可以自己选择，初学的时候需要理解每一个配置是用来做什么的，这点很重要！

  - 代码如下：**wsgi.ini**

    - ```python
           [uwsgi]
           #使用nsinx连接的时候可以使用
           #socket=127.0.0.1:8010

           #直接作为web服务器使用
           http=0.0.0.0:8888

           #配置工程目录
           chdir=/var/www/DjangoAXF/AXF

           #配置项目的wsgi目录，相对于工程目录
           wsgi-file=AXF/wsgi.py

           #配置进程，线程信息
           processes=4
           threads=2
           enable-threads=True
           master=True
           pidfile=uwsgi.pid
           daemonize=uwsgi.log
       ```

- 启动命令

  - ***需要注意在执行命令之前必须吧uwsgi.ini的配置文件放到根目录，然后在跟目录下面执行启动指令***

  - `uwsgi --ini /uwsgi的绝对路径/   #这里是启动命令`

  - `uwsgi --stop uwsgi.pid  #uwsgi的关闭命令，其实就是找到进程号然后杀死进程`  

## uwsgi和nginx对接

- 首先需要先吧前面uwsgi的`socket=127.0.0.1:8010`给启用好，端口是uwsgi的工作端口，可以自定义

- 为nginx进行配置，让nginx可以识别到uwsgi这个模块，一般情况下，uwsgi_params这个模块会内置在nginx的安装目录下，一般就是在`/etc/nginx/`中，我们只需要在nginx.conf的配置文件中将其引用就可以配置好链接的所有需要设置。

-在nginx.conf中为uwsgi设置uwsgi_params模块，和uwsgi_pass的路径，其实就是uwsgi的服务器启动ip和端口号接下来附上一个例子：

```linux

    server {
        listen  80;
        server_name localhost;
        root  /home/Desktop/AXF_project;

        location /static {
            alias /home/Desktop/AXF_project/static
            /*这里的alias是重命名的意思，这样的话程序就会自动吧后面的字符串作为路径来查找了就可以正常使用静态资源了*/

            /*index index.html indet.htm   默认首页，这里是项目静态资源的加载目录所以没有首页也就自动失效了*/

            location /{
                /*这里加载了uwsgi的相关配置为文件需要注意的*/
                include /etc/nginx/uwsgi_params;

                uwsgi_pass  127.0.0.1:8888
                /*注意这里的uwsgi_pass其实就是指我们uwsgi前面设置好的运行ip和端口，这样才可以链接服务器*/
            }
        }
    }

```