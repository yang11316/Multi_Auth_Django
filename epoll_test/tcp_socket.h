#pragma once
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <iostream>
#include <vector>
#include <fcntl.h>
#include <string>

#define CHECK_RET(q)  \
    if ((q) == false) \
    {                 \
        return -1;    \
    }
class TcpSocket
{
public:
    TcpSocket() : socket_fd(-1)
    {
    }

    TcpSocket(int fd)
    {
        this->socket_fd = fd;
    }

    // 生成socket,静态函数，全局可用
    static int generate_socket()
    {
        int tmp_socket = socket(AF_INET, SOCK_STREAM, 0);
        if (tmp_socket < 0)
        {
            perror("socket generate error");
        }
        return tmp_socket;
    }

    bool set_nonblock()
    {
        int old_option = fcntl(this->socket_fd, F_GETFL);
        int new_option = old_option | O_NONBLOCK;
        if (fcntl(this->socket_fd, F_SETFL, new_option) == -1)
        {
            perror("set nonblock error");
            return false;
        }
        return true;
    }

    // 绑定
    bool Bind(std::string &ip, uint16_t port)
    {

        // 绑定前设置端口复用
        int opt = 1;
        if (setsockopt(this->socket_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)))
        {
            perror("setsockopt error");
            return false;
        }

        // 绑定
        struct sockaddr_in addr;
        addr.sin_family = AF_INET;
        addr.sin_port = htons(port);
        addr.sin_addr.s_addr = inet_addr(ip.c_str());
        this->ip = ip;
        this->port = port;

        socklen_t len = sizeof(addr);
        if (bind(this->socket_fd, (struct sockaddr *)&addr, len) < 0)
        {
            perror("bind error");
            return false;
        }
        std::cout << "bind success" << std::endl;
        return true;
    }

    // 监听
    bool Listen(int backlog = 128)
    {
        if (listen(this->socket_fd, backlog) < 0)
        {
            perror("listen error");
            return false;
        }
        std::cout << "listen success" << std::endl;
        return true;
    }

    // 连接
    bool Connect(std::string &ip, uint16_t port)
    {
        struct sockaddr_in addr;
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = inet_addr(ip.c_str());
        addr.sin_port = htons(port);
        socklen_t len = sizeof(addr);

        if (connect(this->socket_fd, (struct sockaddr *)&addr, len) < 0)
        {
            perror("connect error");
            return false;
        }
        std::cout << "connect success" << std::endl;
        return true;
    }

    bool Accept(TcpSocket &sock, struct sockaddr_in *addr = NULL)
    {
        struct sockaddr_in tmp_addr;
        socklen_t len = sizeof(tmp_addr);

        int newfd = accept(this->socket_fd, (struct sockaddr *)&tmp_addr, &len);
        std::cout << newfd << std::endl;
    again:
        if (newfd < 0)
        {
            if ((ECONNABORTED == errno) || (EINTR == errno))
                goto again;
            else
                perror("accept error");
            return false;
        }

        if (addr != NULL)
        {
            memcpy(addr, &tmp_addr, len);
        }
        std::cout << "accept success" << std::endl;
        sock.setsockfd(newfd);
        return true;
    }

    bool Send(const std::string &message)
    {
        if (send(this->socket_fd, message.c_str(), message.size(), 0 < 0) != strlen(message.data()))
        {
            perror("send error");
            return false;
        }
        std::vector<char> buffer(1500);
        ssize_t valread = recv(this->socket_fd, buffer.data(), buffer.size(), 0);
        if (valread < 0)
        {
            perror("send recv error");
            return false;
        }
        std::cout << "get response: " << buffer.data() << std::endl;
        return true;
    }

    bool Read(std::string &buf)
    {
        char tmp[1500] = {0};
        // 接收数据
        ssize_t bytes_received = recv(this->socket_fd, tmp, sizeof(tmp), 0);
        if (bytes_received < 0)
        {
            perror("recv error");
            return false;
        }
        else if (bytes_received == 0)
        {
            std::cout << "client closed" << std::endl;
            return false;
        }

        buf.assign(tmp, bytes_received);
        // 输出接收到的数据
        std::cout << "Received data from client: " << buf << std::endl;
        return true;
    }
    void Close()
    {
        close(socket_fd);
        this->socket_fd = -1;
    }

    pid_t get_current_pid()
    {
        return getpid();
    }
    int getsocketfd()
    {
        return socket_fd;
    }
    void setsockfd(int fd)
    {
        this->socket_fd = fd;
    }

private:
    int socket_fd;
    std::string ip;
    uint16_t port;
};