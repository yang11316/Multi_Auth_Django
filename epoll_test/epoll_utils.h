#pragma once
#include <sys/epoll.h>
#include "tcp_socket.h"

class Epoll
{
private:
    int _epfd;
    int _max_events = 1024;
    struct epoll_event _evs[1024];

public:
    bool Init()
    {
        // 创建epoll实例
        this->_epfd = epoll_create(1);
        if (this->_epfd < 0)
        {
            perror("epoll_create");
            return false;
        }
        return true;
    }
    bool Add(TcpSocket sock, uint32_t events = 0)
    {
        sock.set_nonblock();
        int fd = sock.getsocketfd();
        // 定义事件
        struct epoll_event ev;
        ev.events = EPOLLIN | events;
        ev.data.fd = fd;
        if (epoll_ctl(this->_epfd, EPOLL_CTL_ADD, fd, &ev) < 0)
        {
            perror("epoll_ctl");
            return false;
        }
        return true;
    }
    bool Del(TcpSocket sock)
    {
        int fd = sock.getsocketfd();
        if (epoll_ctl(this->_epfd, EPOLL_CTL_DEL, fd, NULL) < 0)
        {
            perror("epoll_ctl del");
            return false;
        }
        return true;
    }

    bool Wait(std::vector<TcpSocket> &socks, int timeout = -1)
    {
        int nfds = epoll_wait(this->_epfd, this->_evs, this->_max_events, timeout);
        if (nfds < 0)
        {
            perror("epoll_wait error");
            return false;
        }
        else if (nfds == 0)
        {
            return false;
        }
        for (int i = 0; i < nfds; i++)
        {
            int fd = this->_evs[i].data.fd;
            TcpSocket sock(fd);
            socks.push_back(sock);
        }
        return true;
    }
};
