#include "server_socket.h"

TcpServer::TcpServer()
{
}

TcpServer::TcpServer(const std::string &ip, const unsigned int &listening_port)
{
    this->listening_port = listening_port;
    this->ip = ip;
}

TcpServer::~TcpServer()
{
}

int TcpServer::setListen()
{
    int ret = 0;
    struct sockaddr_in saddr;
    memset(&saddr, 0, sizeof(saddr));
    saddr.sin_family = AF_INET;
    saddr.sin_addr.s_addr = inet_addr(ip.c_str());
    saddr.sin_port = htons(listening_port);

    //    创建监听的套接字
    m_lfd = socket(AF_INET, SOCK_STREAM, 0);
    if (m_lfd == -1)
    {
        perror("socket");
        ret = errno;
        return ret;
    }
    int on = 1;
    //    设置端口复用
    ret = setsockopt(m_lfd, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(on));
    if (ret == -1)
    {
        perror("setsockopt");
        ret = errno;
        return ret;
    }
    //    监听的套接字绑定本地IP和端口
    ret = bind(m_lfd, (struct sockaddr *)&saddr, sizeof(saddr));
    if (ret == -1)
    {
        perror("bind");
        ret = errno;
        return ret;
    }
    ret = listen(m_lfd, 128);
    if (ret == -1)
    {
        perror("listen");
        ret = errno;
        return ret;
    }
    return ret;
}

int TcpServer::acceptConn(int wait_time = 10000)
{

    if (wait_time > 0)
    {
        int ret;
        fd_set accept_fdset;
        struct timeval timeout;
        FD_ZERO(&accept_fdset);
        FD_SET(m_lfd, &accept_fdset);
        timeout.tv_sec = wait_time;
        timeout.tv_usec = 0;
        do
        {
            //            检测读集合
            ret = select(m_lfd + 1, &accept_fdset, NULL, NULL, &timeout);
        } while (ret < 0 && errno == EINTR);
        if (ret <= 0)
        {
            return -1;
        }
    }
    // 一但检测出 有select事件发生，表示对等方完成了三次握手，客户端有新连接建立
    // 此时再调用accept将不会堵塞
    struct sockaddr_in addrCli;
    socklen_t addrlen = sizeof(struct sockaddr_in);
    int connfd = accept(m_lfd, (struct sockaddr *)&addrCli, &addrlen); // 返回已连接套接字
    if (connfd == -1)
    {
        return NULL;
    }
    return connfd;
}

void TcpServer::closefd()
{
    close(this->m_lfd);
}
