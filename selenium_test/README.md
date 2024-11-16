本文件夹下仅存放Django+Vue前后端项目的测试代码
/bin/python3 /home/default/Mycode/selenium_test/admin_main.py
/bin/python3 /home/default/Mycode/selenium_test/editor_main.py

selenium_test
├── admin_test.py 管理员侧操作测试
├── config.py 全局配置文件
├── editor_test.py 软件开发人员侧操作测试
├── performance_test.py 2000条数据性能测试
├── README.md
├── requirements.txt 所需依赖
├── user_manage.py 用户管理功能测试
├── node_manage.py 节点管理功能测试
├── software_manage.py 软件管理功能测试
└── entity_manage.py 实体管理功能测试

performance_test
├── run_admin 管理员侧操作测试函数
├── run_editor 软件开发人员侧操作测试函数
└── main

其运行前需先启动整个项目，包含下述四部分：
（1）AS_Server
    cd AS_Server/AS_Server
    python3 manage.py runserver 0.0.0.0:8000

（2）vue-auth-system
    cd Vue/vue-auth-system
    npm run dev

（3）AP_Server
    cd AP_Server
    python3 manage.py runserver 0.0.0.0:9000

（4）process_project
    这里至少启动两个进程，也可自行在process_project编译。用法为（中间均以空格分隔）：./进程名 <要发送的消息> <本地监听IP> <本地监听端口> <本地发送端口> <接收IP> <接收端口> <该域认证代理IP> <该域认证代理端口>
    譬如：
    cd ../file_upload
    ./Process1 hello 0.0.0.0 9999 9994 0 0 0.0.0.0 9000
    
    cd ../file_upload
    ./Process2 hello 0.0.0.0 9998 9994 0.0.0.0 9999 0.0.0.0 9000


而认证库功能的单元测试，位于process_project/crypto_test.cpp
其运行方法为：
    cd process_project
    sudo make .
    sudo cmake
    ./CryptoTest

相应地，该部分测试结果在：
build/gtest_results.json

性能测试部分：
（1）管理员侧：同时访问软件信息管理界面
url: http://localhost:9528/#/software/manage

ab -n 1000 -c 10 -H 'X-token:0ad9e30ca539f968e662b6d505fcd276' -p request_software_manage.json -T application/json http://localhost:9528/#/software/manage > request_software_manage_c{并发数}.txt

（2）软件开发人员侧：同时访问软件注册页面


主要测试参数：
Concurrency Level: 并发的请求数
Time taken for tests: 测试的总时间
Total transferred: 传输的总字节数
Requests per second: 吞吐量，为每秒处理的请求数
Time per request: 
前一行为用户平均请求等待时间，为处理完成所有请求数所花费的时间/（总请求数/并发用户数）
后一行为服务器平均请求等待时间，为处理完成所有请求数所花费的时间/总请求数

响应时间的分布：
50% 的请求，99% 的请求的完成时间