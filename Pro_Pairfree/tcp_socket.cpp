
#include <iostream>
#include "tcp_socket.h"
#include <stddef.h>

TcpSocket::TcpSocket()
{
    this->m_socket = socket(AF_INET, SOCK_STREAM, 0);
}

TcpSocket::TcpSocket(const int &connfd)
{
    this->m_socket = connfd;
}

TcpSocket::~TcpSocket()
{
}

void TcpSocket::bindPort()
{
    // 设置本地地址和端口号
    struct sockaddr_in local_addr;
    memset(&local_addr, '0', sizeof(local_addr));
    local_addr.sin_family = AF_INET;
    local_addr.sin_addr.s_addr = htonl(INADDR_ANY); // 本地地址
    local_addr.sin_port = htons(sending_port);      // 绑定的端口号
    // 设置端口复用
    int opt = 1;
    int ret = setsockopt(this->m_socket, SOL_SOCKET, SO_REUSEADDR, (void *)&opt, sizeof(opt));
    if (ret < 0)
    {
        std::cout << "reuseaddr error:" << errno << std::endl;
    }
    // bind
    ret = bind(this->m_socket, (struct sockaddr *)&local_addr, sizeof(local_addr));
    if (ret < 0)
    {
        std::cout << "bind error:" << errno << std::endl;
    }
}

int TcpSocket::connectToHost(std::string ip, uint16_t port, int timeout)
{
    int ret = 0;
    if (port < 0 || port > 65535 || timeout < 0)
    {
        ret = ParamError;
        return ret;
    }

    if (this->m_socket < 0)
    {
        ret = errno;
        std::cout << "func socket error:" << ret << std::endl;
        return ret;
    }
    struct sockaddr_in saddr;
    saddr.sin_family = AF_INET;
    saddr.sin_port = htons(port);
    saddr.sin_addr.s_addr = inet_addr(ip.data());

    ret = this->connectTimeout((struct sockaddr_in *)&saddr, (unsigned int)timeout);
    if (ret < 0)
    {
        //        超时
        if (ret == -1 && errno == ETIMEDOUT)
        {
            ret = TimeoutError;
            return ret;
        }
        else
        {
            std::cout << "connectTimeout error: " << errno << std::endl;
            return errno;
        }
    }
    return ret;
}

int TcpSocket::sendMsg(std::string data, int timeout)
{
    //    返回0没超时，1超时
    int ret = this->writeTimeout(timeout);
    if (ret == 0)
    {
        int dataLen = data.size();
        ret = writen(data.data(), dataLen);
    }
    else
    { // 失败返回-1，超时返回-1并且errno = ETIMEDOUT
        if (ret == -1 && errno == ETIMEDOUT)
        {
            ret = TimeoutError;
            printf("func sendMsg() Err:%d\n ", ret);
        }
    }
    return ret;
}

int TcpSocket::connectTimeout(struct sockaddr_in *addr, unsigned int wait_seconds)
{
    int ret;
    socklen_t addrlen = sizeof(struct sockaddr_in);
    if (wait_seconds > 0)
    {
        //        需要设置超时等待时，设置为非阻塞模式
        this->setNonBlock(this->m_socket);
    }
    ret = connect(this->m_socket, (struct sockaddr *)addr, addrlen);
    if (ret < 0 && errno == EINPROGRESS)
    {
        fd_set connect_fdset;
        struct timeval timeout;
        //        将连接的描述符集合设为0
        FD_ZERO(&connect_fdset);
        //        将连接描述符加入描述符集合
        FD_SET(this->m_socket, &connect_fdset);
        //        设置等待时间
        timeout.tv_sec = wait_seconds;
        timeout.tv_usec = 0;
        //        使用select循环检测连接是否建立
        do
        {
            ret = select(this->m_socket + 1, NULL, &connect_fdset, NULL, &timeout);
        } while (ret < 0 && errno == EINTR);
        if (ret == 0)
        {
            //            超时
            ret = -1;
            errno = ETIMEDOUT;
        }
        else if (ret < 0)
        {
            return -1;
        }
        else if (ret == 1)
        {
            //            ret返回为1（表示套接字可写），可能有两种情况，一种是连接建立成功，一种是套接字产生错误
            //             此时错误信息不会保存至errno变量中，因此，需要调用getsockopt来获取。
            int err;
            socklen_t sockLen = sizeof(err);
            int sockoptret = getsockopt(this->m_socket, SOL_SOCKET, SO_ERROR, (char *)&err, &sockLen);
            if (sockoptret == -1)
            {
                return -1;
            }
            if (err == 0)
            {
                //            成功建立连接
                ret = 0;
            }
            else
            {
                //            连接失败
                errno = err;
                ret = -1;
            }
        }
    }
    if (wait_seconds > 0)
    {
        //        将套接字重新设置成阻塞模式
        this->setBlock(this->m_socket);
    }
    return ret;
}

int TcpSocket::setNonBlock(int fd)
{
    int flags = fcntl(fd, F_GETFL);
    if (flags == -1)
    {
        return -1;
    }
    flags |= O_NONBLOCK;
    int ret = fcntl(fd, F_SETFL, flags);
    return ret;
}

int TcpSocket::setBlock(int fd)
{
    int ret = 0;
    int flags = fcntl(fd, F_GETFL);
    if (flags == -1)
    {
        return flags;
    }
    flags &= ~O_NONBLOCK;
    ret = fcntl(fd, F_SETFL, flags);
    return ret;
}

int TcpSocket::sendSockmsg(std::string data, int timeout)
{
    //    返回0没超时，1超时
    int ret = this->writeTimeout(timeout);
    if (ret == 0)
    {
        int writed = 0;
        int dataLen = data.size() + 4;
        // 添加4字节作为sock标识  添加4字节作为数据头，存储数据长度
        auto *netdata = (unsigned char *)malloc(dataLen);
        if (netdata == nullptr)
        {
            ret = MallocError;
            printf("func sckClient_send() mlloc Err:%d\n ", ret);
            return ret;
        }
        // 转换为网络字节序
        int netlen = htonl(data.size());

        memcpy(netdata, &netlen, 4);
        memcpy(netdata + 4, data.data(), data.size());
        // 没问题返回发送的实际字节数, 应该 == 第二个参数: dataLen
        // 失败返回: -1
        writed = writen(netdata, dataLen);
        if (writed < dataLen)
        {
            if (netdata != nullptr)
            {
                free(netdata);
                netdata = nullptr;
            }
            return writed;
        }
        if (netdata != nullptr)
        {
            free(netdata);
            netdata = nullptr;
        }
    }
    else
    { // 失败返回-1，超时返回-1并且errno = ETIMEDOUT
        if (ret == -1 && errno == ETIMEDOUT)
        {
            ret = TimeoutError;
            printf("func sckClient_send() mlloc Err:%d\n ", ret);
        }
    }
    return ret;
}

int TcpSocket::sendHttpmsg(std::string post_data, std::string path, const std::string &ip, int timeout)
{
    // 构造http报文

    std::string post_request =
        "POST " + path + " HTTP/1.1\r\n"
                         "Host: " +
        ip +
        "\r\n"
        "Content-Type: text/plain;charset=utf-8\r\n"
        "Content-Length: " +
        std::to_string(post_data.size()) + "\r\n"
                                           "\r\n" +
        post_data;
    // std::cout << post_request << std::endl;
    const char *message = post_request.c_str();
    // 发送http报文
    int ret = this->writeTimeout(timeout);
    if (ret == 0)
    {
        int writed = 0;
        int dataLen = post_request.size();
        writed = writen(message, dataLen);
        if (writed < dataLen)
        {
            return writed;
        }
    }
    else
    { // 失败返回-1，超时返回-1并且errno = ETIMEDOUT
        if (ret == -1 && errno == ETIMEDOUT)
        {
            ret = TimeoutError;
            printf("func sckClient_send() mlloc Err:%d\n ", ret);
        }
    }
    return ret;
}

int TcpSocket::writeTimeout(unsigned int wait_seconds)
{
    int ret = 0;
    if (wait_seconds > 0)
    {
        fd_set write_fdset;
        struct timeval timeout;

        FD_ZERO(&write_fdset);
        FD_SET(m_socket, &write_fdset);
        timeout.tv_sec = wait_seconds;
        timeout.tv_usec = 0;
        do
        {
            ret = select(m_socket + 1, NULL, &write_fdset, NULL, &timeout);
        } while (ret < 0 && errno == EINTR);
        // 超时
        if (ret == 0)
        {
            ret = -1;
            errno = ETIMEDOUT;
        }
        else if (ret == 1)
        {
            ret = 0; // 没超时
        }
    }
    return ret;
}

std::string TcpSocket::recvSockmsg(int timeout)
{
    // 返回0 -> 没超时就接收到了数据, -1, 超时或有异常
    int ret = this->readTimeout(timeout);
    if (ret != 0)
    {
        if (ret == -1 || errno == ETIMEDOUT)
        {
            printf("readTimeout(timeout) err: TimeoutError \n");
            return {};
        }
        else
        {
            printf("readTimeout(timeout) err: %d \n", ret);
            return {};
        }
    }

    int netdatalen = 0;
    ret = this->readn(&netdatalen, 4); // 读包头 4个字节
    if (ret == -1)
    {
        std::cout << "func readn() err:" << ret << std::endl;
        return {};
    }
    else if (ret < 4)
    {
        std::cout << "func readn() err peer closed:" << ret << std::endl;
        return {};
    }
    int n = ntohl(netdatalen);
    // 根据包头中记录的数据大小申请内存, 接收数据
    char *tmpBuf = (char *)malloc(n);
    if (tmpBuf == NULL)
    {
        ret = MallocError;
        std::cout << "malloc() err " << std::endl;
        return {};
    }
    ret = readn(tmpBuf, n); // 根据长度读数据
    if (ret == -1)
    {
        std::cout << "func readn() err:%d" << std::endl;
        return {};
    }
    else if (ret < n)
    {
        std::cout << "func readn() err peer closed:" << std::endl;
        return {};
    }
    tmpBuf[n] = '\0'; // 多分配一个字节内容，兼容可见字符串 字符串的真实长度仍然为n
    std::string data = std::string(tmpBuf, n);
    // 释放内存
    free(tmpBuf);

    return data;
}

std::string TcpSocket::recvmsg(int recv_len, int timeout)
{
    // 返回0 -> 没超时就接收到了数据, -1, 超时或有异常
    int ret = this->readTimeout(timeout);
    if (ret != 0)
    {
        if (ret == -1 || errno == ETIMEDOUT)
        {
            printf("readTimeout(timeout) err: TimeoutError \n");
            return {};
        }
        else
        {
            printf("readTimeout(timeout) err: %d \n", ret);
            return {};
        }
    }
    // 读取全部数据
    if (recv_len == 0)
    {
        int buffer_size = 4096;
        char buffer[buffer_size];
        ret = read(m_socket, buffer, buffer_size);
        std::cout << "recv ret:" << ret << std::endl;
        if (ret == -1)
        {
            perror("read() err");
        }

        std::string data = std::string(buffer, ret);

        return data;
    }

    char *tmpBuf = (char *)malloc(recv_len);
    ret = this->readn(tmpBuf, recv_len);
    if (ret == -1)
    {
        perror("readn() err");
    }
    else if (ret < recv_len)
    {
        perror("readn() err");
    }
    std::string data = std::string(tmpBuf, ret);
    free(tmpBuf);
    return data;
}

std::string TcpSocket::recvHTTPmsg(int timeout)
{
    int ret = this->readTimeout(timeout);
    if (ret != 0)
    {
        if (ret == -1 || errno == ETIMEDOUT)
        {
            printf("readTimeout(timeout) err: TimeoutError \n");
            return {};
        }
        else
        {
            printf("readTimeout(timeout) err: %d \n", ret);
            return {};
        }
    }

    std::string response;
    char buffer[4096];
    int bytesReceived;
    // 循环读取直到获取完整的响应
    while ((bytesReceived = recv(m_socket, buffer, sizeof(buffer) - 1, 0)) > 0)
    {
        buffer[bytesReceived] = '\0'; // 确保字符串结束
        response += buffer;

        // 检查是否已经读取到完整的HTTP头部
        if (response.find("\r\n\r\n") != std::string::npos)
        {
            break; // 找到头部结束标志
        }
    }
    // 提取内容长度
    size_t contentLength = 0;
    size_t headerEndPos = response.find("\r\n\r\n");

    if (headerEndPos != std::string::npos)
    {
        std::string headers = response.substr(0, headerEndPos);
        size_t pos = headers.find("Content-Length:");

        if (pos != std::string::npos)
        {
            size_t start = headers.find_first_not_of(" \t", pos + 15); // 跳过 "Content-Length: "
            size_t end = headers.find_first_of("\r\n", start);
            contentLength = std::stoul(headers.substr(start, end - start));
        }

        // 读取主体
        response.erase(0, headerEndPos + 4); // 移除头部
        while (response.size() < contentLength)
        {
            bytesReceived = recv(m_socket, buffer, sizeof(buffer) - 1, 0);
            buffer[bytesReceived] = '\0';
            response += buffer;
        }
    }
    return response;
}

int TcpSocket::readTimeout(unsigned int wait_seconds)
{
    int ret = 0;
    if (wait_seconds > 0)
    {
        fd_set read_fdset;
        struct timeval timeout;

        FD_ZERO(&read_fdset);
        FD_SET(m_socket, &read_fdset);
        timeout.tv_sec = wait_seconds;
        timeout.tv_usec = 0;
        // select返回值三态
        // 1 若timeout时间到（超时），没有检测到读事件 ret返回=0
        // 2 若ret返回<0 &&  errno == EINTR 说明select的过程中被别的信号中断（可中断睡眠原理）
        // 2-1 若返回-1，select出错
        // 3 若ret返回值>0 表示有read事件发生，返回事件发生的个数
        do
        {
            ret = select(m_socket + 1, &read_fdset, NULL, NULL, &timeout);
        } while (ret < 0 && errno == EINTR);
        // 超时
        if (ret == 0)
        {
            ret = -1;
            errno = ETIMEDOUT;
        }
        else if (ret == 1)
        {
            ret = 0; // 没超时
        }
    }
    return ret;
}

void TcpSocket::disConnect()
{
    if (this->m_socket >= 0)
    {
        close(m_socket);
    }
}

int TcpSocket::getSocket()
{
    return m_socket;
}

void TcpSocket::setSendingPort(uint16_t port)
{
    this->sending_port = port;
}

// 成功返回count，失败返回-1，读到EOF返回<count
int TcpSocket::readn(void *buf, int count)
{
    size_t nleft = count;
    ssize_t nread;
    char *bufp = (char *)buf;
    while (nleft > 0)
    {
        if ((nread = read(m_socket, bufp, nleft)) < 0)
        {
            if (errno == EINTR)
            {
                continue;
            }
            return -1;
        }
        else if (nread == 0)
        {
            return count - nleft;
        }
        bufp += nread;
        nleft -= nread;
    }
    return count;
}
// 成功返回count，失败返回-1
int TcpSocket::writen(const void *buf, int count)
{
    size_t nleft = count;
    ssize_t nwritten;
    char *bufp = (char *)buf;

    while (nleft > 0)
    {
        if ((nwritten = write(m_socket, bufp, nleft)) < 0)
        {
            if (errno == EINTR) // 被信号打断
            {
                continue;
            }
            return -1;
        }
        else if (nwritten == 0)
        {
            continue;
        }

        bufp += nwritten;
        nleft -= nwritten;
    }
    return count;
}
