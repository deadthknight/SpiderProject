### 查看Python3查的证书
```shell
[root@rocky1 ~]# python3
Python 3.8.13 (default, Nov  8 2022, 17:19:05)
[GCC 8.5.0 20210514 (Red Hat 8.5.0-15)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import certifi
>>> certifi.where()
'/usr/local/lib/python3.8/site-packages/certifi/cacert.pem'

```

### 写入根证书
```shell
# 已经提前把CA的根证书放到了/root目录
[root@rocky1 ~]# ls
 root.cer

# 把根证书写入cacert.pem
[root@rocky1 ~]# cat root.cer >> /usr/local/lib/python3.8/site-packages/certifi/cacert.pem

```

### 测试requests
```shell
[root@rocky1 ~]# python3
Python 3.8.13 (default, Nov  8 2022, 17:19:05)
[GCC 8.5.0 20210514 (Red Hat 8.5.0-15)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import requests
>>> r = requests.get('https://flask.netdevops.com')
>>> print(r)
<Response [200]>

```