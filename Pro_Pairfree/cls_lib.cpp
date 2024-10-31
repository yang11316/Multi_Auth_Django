#include "cls_lib.h"

CLS_LIB::CLS_LIB(std::string jsonFile)
{
    std::ifstream ifs(jsonFile);
    Json::Reader reader;
    Json::Value root;
    reader.parse(ifs, root);
    this->ip = root["ip"].asString();
    this->listening_port = root["listening_port"].asUInt();
    this->sending_port = root["sending_port"].asUInt();
    this->ap_ip = root["ap_ip"].asString();
    this->ap_port = root["ap_port"].asUInt();
    this->m_process_manager = new Process_manager;
}
CLS_LIB::CLS_LIB(const std::string &ip, const uint16_t &listening_port, const uint16_t &sending_port, const std::string &ap_ip, const uint16_t &ap_port)
{
    this->ip = ip;
    this->listening_port = listening_port;
    this->sending_port = sending_port;
    this->ap_ip = ap_ip;
    this->ap_port = ap_port;
    this->m_process_manager = new Process_manager;
}

bool CLS_LIB::init()
{

    // 发送http请求
    std::cout << "connect to AP" << std::endl;
    this->m_socket = new TcpSocket();
    m_socket->setSendingPort(sending_port);
    m_socket->bind();

    if (m_socket->connectToHost(ap_ip, ap_port, 0) < 0)
    {
        perror("connect to ap failed");
        return false;
    }

    std::string post_data = "{\"process_id\":" + std::to_string(get_current_pid()) + ",\"listening_port\":" + std::to_string(listening_port) + ",\"sending_port\":" + std::to_string(sending_port) + "}";
    std::string path = "/entitymanage/sendparticalkeyandpid/";
    m_socket->sendHttpmsg(post_data, path, ip);
    std::string recv_msg = m_socket->recvHTTPmsg();
    if (recv_msg == "error")
    {
        m_socket->disConnect();
        return false;
    }
    Json::Reader reader;
    Json::Value root;
    Json::Value value;
    // 使用jsoncpp解析json数据
    if (reader.parse(recv_msg, root))
    {
        value = root["entity_data"];
        for (auto val : value)
        {
            std::string pid = val["pid"].asCString();
            std::string parcial_key = val["entity_parcialkey"].asCString();
            std::string acc_publickey = val["acc_publickey"].asCString();
            std::string acc_cur = val["acc_cur"].asCString();
            std::string kgc_Ppub = val["kgc_Ppub"].asCString();
            Process tmp_process(pid, acc_publickey, acc_cur, parcial_key, kgc_Ppub);
            if (tmp_process.generate_full_key())
            {
                std::cout << "generate full key success with pid:" << pid << std::endl;
                this->m_process_manager->push_back(tmp_process);
            }
            else
            {
                std::cout << "[Error] generate full key failed with parcialkey: " << pid << std::endl;
            }
        }
    }

    m_socket->disConnect();
    return true;
}

std ::string CLS_LIB::sign(const std::string &msg)
{
    if (this->m_process_manager->get_size() > 0)
    {
        // std::cout << "====================Send Sign Message====================" << std::endl;
        sign_payload payload = this->m_process_manager->get_process().sign(msg);
        // std::cout << payload.to_string() << std::endl;
        std::string msg_str = "pid=" + payload.pid + "&msg=" + payload.msg + "&sig1=" + payload.sig1 + "&sig2=" + payload.sig2 + "&time_stamp=" + payload.time_stamp + "&WIT=" + payload.WIT + "&wit_hex=" + payload.wit_hex + "&X=" + payload.X;
        return msg_str;
    }
    else
    {
        std::cout << "[ERROR] parcial key not enough" << std::endl;
        return {};
    }
}

bool CLS_LIB::verify(const std::string &sig)
{
    if (this->m_process_manager->get_size() > 0)
    {
        Process tmp_process = this->m_process_manager->get_process();
        std::unordered_map<std::string, std::string> payload_map = parse_form_socket(sig);
        sign_payload recv_payload;
        recv_payload.pid = payload_map["pid"];
        recv_payload.msg = payload_map["msg"];
        recv_payload.sig1 = payload_map["sig1"];
        recv_payload.sig2 = payload_map["sig2"];
        recv_payload.time_stamp = payload_map["time_stamp"];
        recv_payload.WIT = payload_map["WIT"];
        recv_payload.wit_hex = payload_map["wit_hex"];
        recv_payload.X = payload_map["X"];

        return tmp_process.verify_sign(recv_payload);
    }
    else
    {
        std::cout << "[ERROR] parcial key not enough" << std::endl;
        return false;
    }
}

void CLS_LIB::startListening()
{

    if (m_server != nullptr)
    {
        perror("server has been started");
        return;
    }
    m_server = new TcpServer(ip, listening_port);
    // 设置监听
    int ret = m_server->setListen();
    int m_fd = m_server->getSocket();
    // 使用select监听
    fd_set read_fd;
    FD_ZERO(&read_fd);
    fd_set tmp_set;
    FD_ZERO(&tmp_set);
    // 将套接字放入文件描述集合终
    FD_SET(m_fd, &read_fd);
    int max_sd = m_fd;
    while (1)
    {
        int client_socket = m_server->acceptConn(0);
        if (client_socket <= 0)
        {
            continue;
        }
        std::thread client_thread(&CLS_LIB::client_deal, this, client_socket);
        client_thread.join();
    }
}

void CLS_LIB::client_deal(int connfd)
{
    int client_socket = connfd;
    TcpSocket *new_socket = new TcpSocket(client_socket);
    // string tmp_flag = new_socket->recvmsg(4, 0);
    // cout << "receive flag: " << tmp_flag << endl;
    // if (tmp_flag == "POST")
    // {
    // cout << "receive http request" << endl;
    std::string recv_msg = new_socket->recvmsg(0, 0);
    std::cout << "receive http message:" << recv_msg << std::endl;
    std::unordered_map<std::string, std::string> tmp_params = parse_from_http(recv_msg);
    // cout << tmp_params.size() << endl;

    // 更新消息
    if (tmp_params.size() == 1)
    {
        if (this->m_process_manager->get_size() > 0)
        {
            this->m_process_manager->update_process(tmp_params["aux"]);
            std::cout << "partical key update" << std::endl;
            std::cout << "accumulator:" << m_process_manager->get_process().acc_cur.get_str(16) << std::endl;
        }
    }
    // 参数消息 暂时无用
    else if (tmp_params.size() == 5)
    {
        Process tmp_process(tmp_params["pid"], tmp_params["acc_publickey"], tmp_params["acc_cur"], tmp_params["entity_parcialkey"], tmp_params["kgc_Ppub"]);
        //
        if (tmp_process.generate_full_key())
        {
            std::cout << "generate full key success" << std::endl;
            this->m_process_manager->push_back(tmp_process);
        }
        else
        {
            std::cout << "[Error] generate full key failed with parcialkey: " << tmp_params["entity_parcialkey"] << std::endl;
        }
    }
    std::string response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n";
    new_socket->sendMsg(response);
    new_socket->disConnect();
    return;
}

CLS_LIB::~CLS_LIB()
{
    if (m_server)
    {
        m_server->closefd();
        delete m_server;
        m_server = nullptr;
    }
}

pid_t CLS_LIB::get_current_pid()
{
    return getpid();
}

std::unordered_map<std::string, std::string> CLS_LIB::parse_from_http(const std::string &http_data)
{
    std::unordered_map<std::string, std::string> result;
    size_t pos = http_data.find("\r\n\r\n");
    std::cout << pos << std::endl;
    if (pos != std::string::npos)
    {
        // 获取json格式数据
        std::string data = http_data.substr(pos + 4);
        // 按 '&' 分割数据
        pos = 0;
        while (pos < data.size())
        {
            size_t end_pos = data.find('&', pos);
            if (end_pos == std::string::npos)
            {
                end_pos = data.size();
            }
            std::string pair = data.substr(pos, end_pos - pos);

            // 按 '=' 分割键值对
            size_t equal_pos = pair.find('=');
            if (equal_pos != std::string::npos)
            {
                std::string key = pair.substr(0, equal_pos);
                std::string value = pair.substr(equal_pos + 1);

                // URL 解码
                // 这里省略了 URL 解码的步骤，
                // 存储键值对
                result[key] = value;
            }
            pos = end_pos + 1;
        }
    }
    return result;
}

std::unordered_map<std::string, std::string> CLS_LIB::parse_form_socket(const std::string &socket_data)
{
    std::unordered_map<std::string, std::string> result;
    // 获取json格式数据
    // 按 '&' 分割数据
    int pos = 0;
    while (pos < socket_data.size())
    {
        size_t end_pos = socket_data.find('&', pos);
        if (end_pos == std::string::npos)
        {
            end_pos = socket_data.size();
        }
        std::string pair = socket_data.substr(pos, end_pos - pos);

        // 按 '=' 分割键值对
        size_t equal_pos = pair.find('=');
        if (equal_pos != std::string::npos)
        {
            std::string key = pair.substr(0, equal_pos);
            std::string value = pair.substr(equal_pos + 1);
            // 存储键值对
            result[key] = value;
        }
        pos = end_pos + 1;
    }

    return result;
}

bool CLS_LIB::open_port(std::vector<uint16_t> &port)
{
    // 发送http请求
    std::cout << "connect to AP" << std::endl;
    this->m_socket = new TcpSocket();
    m_socket->setSendingPort(sending_port);
    m_socket->bind();
    if (m_socket->connectToHost(ap_ip, ap_port, 0) < 0)
    {
        perror("connect to ap failed");
        return false;
    }
    int processid = this->get_current_pid();
    std::string post_data = "{\"process_id\":" + std::to_string(get_current_pid()) + ",\"open_port\":[";
    for (auto i : port)
    {
        post_data += std::to_string(i) + ",";
    }
    post_data.pop_back();
    post_data += "]}";
    std::string path = "/entitymanage/getopenport/";
    m_socket->sendHttpmsg(post_data, path, ip);
    if (m_socket->recvHTTPmsg(0) == "success")
    {
        return true;
    }
    return false;
}

bool CLS_LIB::delete_key(const std::string &pid)
{
    if (this->m_process_manager->delete_process(pid))
    {
        return true;
    }
    return false;
}

int CLS_LIB::get_key_size()
{
    return this->m_process_manager->get_size();
}
