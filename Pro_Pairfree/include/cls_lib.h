
#ifndef CLS_LIB_H
#define CLS_LIB_H

#include "base_thread.h"
#include "server_socket.h"
#include "process_parifree.h"
#include <unordered_map>
#include "json/json.h"
#include <fstream>
#include <sys/select.h>

/*
dds_type:
    1:publisher 发布消息
    2:subscriber 订阅消息
protocol_type:
    1:tcp
    2:udp
*/
struct dds_info
{
    int dds_type;
    int protocol_type;
    std::string source_ip;
    int source_port;
    std::string source_mask;
    std::string source_mac;

    std::string destination_ip;
    int destination_port;
    std::string destination_mask;
    std::string destination_mac;

    dds_info()
    {
        dds_type = -1;
        protocol_type = -1;
        source_ip = "0.0.0.0";
        source_port = -1;
        source_mask = "255.255.255.255";
        source_mac = "00:00:00:00:00:00";
        destination_ip = "0.0.0.0";
        destination_port = -1;
        destination_mask = "255.255.255.255";
        destination_mac = "00:00:00:00:00:00";
    }
};

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
    void run() override;

    // 初始化认证库
    bool init();
    // 获取一个可用的认证库句柄pid
    std::string get_process_pid();
    // 签名
    std::string sign(const std::string &pid, const std::string &msg);
    // 验签
    bool verify(const std::string &pid, const std::string &sig);
    // 发送DDS要订阅或发布的ip等数据,dds_type 0:发布，1:订阅
    bool send_DDS_info(const std::string &pid, const dds_info &info);

    // 查看当前系统有多少可用的
    int get_avaliable_process_size();

    bool delete_key(const std::string &pid);

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