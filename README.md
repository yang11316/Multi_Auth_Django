# 环境依赖

## Python 环境

| Python 3.10.12             |
| -------------------------- |
| django   4.0               |
| django-apscheduler  0.6.2  |
| django-cors-headers  4.3.1 |
| gmpy2   2.1.5              |
| fastecdsa  2.2.3           |
| cryptography  3.4.8        |
| scapy                      |

## c++依赖

| g++ 环境       |
| -------------- |
| openssl 3.0.10 |
| gmp 6.2.1      |
| jsoncpp 1.9.5  |



## Vue环境

| npm：8.19.4          |
| -------------------- |
| Node.js：16.20.0 LTS |
| vue-cli：4.5.19      |

## Mysql环境

| mysql 8.0.39 |
| ------------ |
|              |





# AS配置

进入AS_Server目录下，修改settings.py文件

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",  # 默认
        "NAME": "django_db",  # 连接的数据库  #一定要存在的数据库名
        "HOST": "127.0.0.1",  # mysql的ip地址
        "PORT": 3306,  # mysql的端口
        "USER": "root",  # mysql的用户名
        "PASSWORD": "*****",  # mysql的密码
    }
}
```

```
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:9528",  # 替换成自己的前端url
]
CORS_ORIGIN_WHITELIST = [
    "https://localhost:9528",
    "http://localhost:9528",
    "http://192.168.3.17:9528",# 替换成自己的ip
    "https://192.168.3.17:9528",
]
```



# AP配置

打开seetings.py文件

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",  # 默认
        "NAME": "django_ap_db",  # 连接的数据库  
        "HOST": "127.0.0.1",  # mysql的ip地址
        "PORT": 3306,  # mysql的端口
        "USER": "root",  # mysql的用户名
        "PASSWORD": "******",  # mysql的密码
    }
}
```

```
#设置AS的ip和端口
AS_IP="192.168.3.17"
AS_PORT=8000
```



# 认证库接口及使用



使用cmake要链接的库

```
set(Openssl_INCLUDE_DIR /usr/local/openssl/include)
set(Openssl_LIB_DIR /usr/local/openssl/lib64)

include_directories(${Openssl_INCLUDE_DIR})

target_link_libraries(文件名  ${Openssl_LIB_DIR}/libssl.a ${Openssl_LIB_DIR}/libcrypto.a pthread libjsoncpp.a dl gmp gmpxx)
```



## 接口

| 函数                                                         | 作用                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| bool init();                                                 | 初始化认证库，会主动与ap通信                                 |
| std::string get_process_pid();                               | 获取一个无证书身份的句柄，后面接口用其作为参数               |
| std::string sign(const std::string &pid, const std::string &msg); | 签函函数<br />pid：身份的句柄，上一个函数返回值<br />msg：签名信息 |
| bool verify(const std::string &pid, const std::string &sig); | 验证签名函数<br />pid：身份句柄<br />sig：签名消息           |
| bool send_DDS_info(const std::string &pid, const dds_info &info); | 向交换机发送dds的信息<br />pid：身份的句柄<br />info：数据结构，见下 |
| int get_avaliable_process_size();                            | 查看当前认证库有多少可用的身份                               |

数据结构

```
struct dds_info
{
	// dds_type: 1表示publisher；2表示subscriber
    int dds_type; 
    // protocol_type：1表示tcp；2表示udp
    int protocol_type;
    
    //源信息，mask可以默认填“255.255.255.255”
    std::string source_ip;
    int source_port;
    std::string source_mask;
    std::string source_interface;
	
	//目的信息，mask可以默认填“255.255.255.255”
    std::string destination_ip;
    int destination_port;
    std::string destination_mask;
    std::string destination_mac;
}
```

