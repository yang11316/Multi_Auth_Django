
#ifndef CLS_LIB_H
#define CLS_LIB_H

#include "server_socket.h"
#include "process_parifree.h"
#include "data_buffer.h"
#include <queue>
#include <mutex>
#include <condition_variable>
#include <unordered_map>
#include <string>
#include <thread>
using namespace std;

class CLS_LIB
{
private:
    unsigned int sending_port;
    unsigned int listening_port;
    std::string ip;
    std::string ap_ip;
    unsigned int ap_port;

    TcpServer *m_server = nullptr;
    Process *m_process = nullptr;
    TcpSocket *m_socket = nullptr;

    // 两个缓冲区：http参数缓冲区，socket缓冲区
    DataBuffer http_queue;

public:
    CLS_LIB(string json_file);
    // 启动服务器
    void startListening();
    bool init();
    string sign(string msg);
    bool verify(string sig);

    ~CLS_LIB();

private:
    void deal_socketmsg(TcpSocket *sock);

    // 接收消息，并放入不同的缓冲区
    void client_deal(int connfd);
    // 获取当前进程号
    pid_t get_current_pid();
    // 解析http数据
    std::unordered_map<std::string, std::string> parse_from_http(const std::string &http_data);
    // 解析socket传来的数据
    std::unordered_map<std::string, std::string> parse_form_socket(const std::string &socket_data);
};

#endif