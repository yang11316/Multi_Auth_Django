#ifndef TCP_SOCKET_H
#define TCP_SOCKET_H
// 用于通信的套接字类

#include <string>
#include <unistd.h>
#include <sys/types.h>
#include <fcntl.h>
#include <sys/time.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <sys/select.h>
#include <stdio.h>

// 超时时间
static const int TIMEOUT = 10000;

class TcpSocket
{
public:
    enum ErrorType
    {
        ParamError = 3001,
        TimeoutError,
        PeerCloseError,
        MallocError
    };
    TcpSocket();
    //    使用一个可以用于通信的套接字实例化套接字对象
    TcpSocket(const int &connfd);
    ~TcpSocket();

    // 绑定发送端口
    void bind();
    // 链接服务器
    int connectToHost(std::string ip, uint16_t port, int timeout = TIMEOUT);

    // 发送没有格式要求的数据
    int sendMsg(std::string data, int timeout = TIMEOUT);

    // 发送socket数据
    int sendSockmsg(std::string data, int timeout = TIMEOUT);

    // 发送Http数据
    int sendHttpmsg(std::string post_data, std::string path, const std::string &ip, int timeout = TIMEOUT);

    // 接收数据
    std::string recvSockmsg(int timeout = TIMEOUT);
    // 接收指定长度数据，n字节
    std::string recvmsg(int recv_len = 0, int timeout = TIMEOUT);

    std::string recvHTTPmsg(int timeout = TIMEOUT);

    // 断开连接
    void disConnect();

    int getSocket();
    void setSendingPort(uint16_t port);

private:
    // 设置IO为非阻塞模式
    int setNonBlock(int fd);
    // 设置IO为阻塞模式
    int setBlock(int fd);
    // 读超时检测函数，不含读操作
    int readTimeout(unsigned int wait_seconds);
    // 写超时检测函数, 不包含写操作
    int writeTimeout(unsigned int wait_seconds);
    // 带连接超时的connect函数
    int connectTimeout(struct sockaddr_in *addr, unsigned int wait_seconds);
    // 每次从缓冲区读n个字符
    int readn(void *buf, int count);
    // 每次往缓冲区写入n个字符
    int writen(const void *buf, int count);

private:
    int m_socket;
    uint16_t sending_port;
};

#endif // TCP_SOCKET_H
