#ifndef SERVER_SOCKET_H
#define SERVER_SOCKET_H
#include "tcp_socket.h"
class TcpServer
{
private:
    int m_lfd;
    unsigned int listening_port;
    std::string ip;

public:
    TcpServer();
    TcpServer(const std::string &ip, const unsigned int &listening_port);
    ~TcpServer();

    //    服务器设置监听
    int setListen();
    //    等待并接受客户端连接请求，默认连接时间为timeout，超时退出listening
    int acceptConn(int timeout);

    void closefd();
};

#endif