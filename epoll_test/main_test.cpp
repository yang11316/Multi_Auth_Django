#include "tcp_socket.h"
#include "epoll_utils.h"

int main()
{
    TcpSocket server;
    server.setsockfd(server.generate_socket());
    std::string ip = "127.0.0.1";
    CHECK_RET(server.Bind(ip, 9000));
    CHECK_RET(server.Listen());

    Epoll epoll;
    CHECK_RET(epoll.Init());
    CHECK_RET(epoll.Add(server, EPOLLET));
    std::vector<TcpSocket> list;
    while (1)
    {
        bool ret = epoll.Wait(list);
        if (ret == false)
        {
            continue;
        }
        std::cout << "wait sucess" << std::endl;
        for (int i = 0; i < list.size(); i++)
        {
            if (list[i].getsocketfd() == server.getsocketfd())
            {
                std::cout << "accept a new client" << std::endl;
                TcpSocket tmp_client;
                server.Accept(tmp_client);
                epoll.Add(tmp_client, EPOLLET);
            }
            else
            {
                std::string buf;
                list[i].Read(buf);
                std::cout << buf << std::endl;
            }
        }
        list.clear();
    }
    server.Close();
    return 0;
}