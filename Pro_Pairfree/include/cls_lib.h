
#ifndef CLS_LIB_H
#define CLS_LIB_H

#include "base_thread.h"
#include "server_socket.h"
#include "process_parifree.h"
#include <unordered_map>
#include "json/json.h"
#include <fstream>
#include <sys/select.h>

class CLS_LIB : public BaseThread
{
private:
    uint16_t sending_port;
    uint16_t listening_port;
    std::string ip;
    std::string ap_ip;
    uint16_t ap_port;

    TcpServer *m_server = nullptr;
    TcpSocket *m_socket = nullptr;
    Process_manager *m_process_manager = nullptr;

    std::string domain_id;

public:
    CLS_LIB(std::string json_file);
    CLS_LIB(const std::string &ip, const uint16_t &listening_port, const uint16_t &sending_port, const std::string &ap_ip, const uint16_t &ap_port);
    // 禁止拷贝
    CLS_LIB(const CLS_LIB &) = delete;
    CLS_LIB &operator=(const CLS_LIB &) = delete;
    ~CLS_LIB();

    // 启动服务器
    // void startListening();
    void run() override;
    bool init();
    std::string sign(const std::string &msg);
    bool verify(const std::string &sig);
    bool open_port(std::vector<uint16_t> &port);
    bool delete_key(const std::string &pid);
    int get_key_size();

private:
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