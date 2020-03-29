# 使用nginx对接runserver

## 反向代理

- proxy_pass URL;  反向代理转发的地址，默认不转发header,需要转发header则设置proxy_set_header HOST $host;

- proxy_method POST;  转发的方法名

- proxy_hide_header Cache_Control;  指定头部不被转发

- proxy_pass_header Cache_Control;设置那些头部转发

- proxy_pass_request_header on; 设置转发http请求头

- proxy_pass_request_body on;  设置转发请求体

## 加入你需要为自己的runserver服务器配置一下，让nginx也可以直接解析你的服务器那么你就可以这样做！

- `python manager.py runserver 9000`  设置服务器在9000端口执行

- 既然想要nginx为你的runserver服务器工作，自然就需要配置一下nginx了

  - 配置`location / { proxy_pass http://localhost:9000; }`

## upstream（负载均衡）

- 负载均衡模块，通过一个简单的调度算法来实现客户ip到后端服务器的负载平衡

- 写法

    upstream myproject{
        ip_hash;
        server 127.0.0.1:8000;
        server 127.0.0.1:8001 down;
        server 127.0.0.1:8002 weight=3;
        server 127.0.0.1:8003 backup;
        fair;
    }

- 负载均衡算法
  - weight 负载权重
  - down 当前server不参与负载均衡
  - backup 当其他机器全down掉或者满载使用此服务
  - ip_hash 按照每个请求的hash结果分配
  - fair    按后端响应时间来分（第三方的）

### 负载均衡的实例

- 我们只需要在nginx.conf的配置文件中添加一个负载均衡模块，然后添加相关路由即可！

    upstream myserver{
        server 127.0.0.1:8000;
        server 127.0.0.1:8001;
        server 127.0.0.1:8002;
    }

  - 需要注意的是负载均衡模块是放在server模块之外的并且在http模块里面(其实很好理解，http是负责服务器转发的模块，负载均衡理应由他负责)，而location是在server里面的

    location / {

        proxy_pass http://myserver;

    **很重要的提示：负载均衡模块的命令不可以包含下划线，切记不可以包含下划线！**

    }
