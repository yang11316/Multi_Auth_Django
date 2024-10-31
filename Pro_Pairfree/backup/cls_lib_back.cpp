#include "cls_lib.h"

CLS_LIB::CLS_LIB(string jsonFile)
{
    ifstream ifs(jsonFile);
    Json::Reader reader;
    Json::Value root;
    reader.parse(ifs, root);
    this->ip = root["ip"].asString();
    this->listening_port = root["listening_port"].asUInt();
    this->sending_port = root["sending_port"].asUInt();
    this->ap_ip = root["ap_ip"].asString();
    this->ap_port = root["ap_port"].asUInt();
    this->m_process = new Process();
}

bool CLS_LIB::init()
{

    // 发送http请求
    std::cout << "connect to AP" << endl;
    this->m_socket = new TcpSocket();
    m_socket->setSendingPort(sending_port);
    m_socket->bind();

    if (m_socket->connectToHost(ap_ip, ap_port, 0) < 0)
    {
        perror("connect to ap failed");
        return false;
    }
    m_socket->sendHttpmsg(get_current_pid(), ip, listening_port);
    m_socket->disConnect();

    // 检测缓冲区内是否有数据,有则读取，没有则等待
    string http_msg = http_queue.popData();
    std::unordered_map<std::string, std::string> tmp_params = parse_from_http(http_msg);
    std::cout << http_msg << endl;
    this->m_process->init(tmp_params["pid"], tmp_params["acc_publickey"], tmp_params["acc_cur"], tmp_params["entity_parcialkey"], tmp_params["kgc_Ppub"]);
    if (!this->m_process->generate_full_key())
    {
        cout << "generate full key failed" << endl;
        return false;
    }
    return true;
}

string CLS_LIB::sign(string msg)
{
    if (this->m_process->is_fullkey)
    {
        std::cout << std::endl;
        std::cout << "====================Send Sign Message====================" << std::endl;
        sign_payload payload = this->m_process->sign(msg);
        std::cout << payload.to_string() << std::endl;
        std::string msg_str = "pid=" + payload.pid + "&msg=" + payload.msg + "&sig1=" + payload.sig1 + "&sig2=" + payload.sig2 + "&time_stamp=" + payload.time_stamp + "&WIT=" + payload.WIT + "&wit_hex=" + payload.wit_hex + "&X=" + payload.X;
        return msg_str;
    }
    else
    {
        cout << "not generate full key" << endl;
        return {};
    }
}

bool CLS_LIB::verify(string sig)
{
    if (this->m_process->is_fullkey)
    {
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
        return this->m_process->verify_sign(recv_payload);
    }
    else
    {
        cout << "not generate full key" << endl;
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
    string recv_msg = new_socket->recvmsg(0, 0);
    // cout << "receive http message:" << recv_msg << endl;
    std::unordered_map<std::string, std::string> tmp_params = parse_from_http(recv_msg);
    // cout << tmp_params.size() << endl;

    // 更新消息
    if (tmp_params.size() == 1)
    {
        if (this->m_process->is_init)
        {
            this->m_process->update_key(tmp_params["aux"]);
            std::cout << "partical key update" << std::endl;
            std::cout << "accumulator:" << m_process->acc_cur.get_str(16) << std::endl;
        }
    }
    // 参数消息
    else if (tmp_params.size() == 5)
    {
        this->http_queue.pushData(recv_msg);
    }
    string response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n";
    new_socket->sendMsg(response);
    // }
    new_socket->disConnect();
    delete new_socket;
    new_socket = nullptr;
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

            // URL 解码
            // 这里省略了 URL 解码的步骤，你可以根据需要实现

            // 存储键值对
            result[key] = value;
        }
        pos = end_pos + 1;
    }

    return result;
}

void CLS_LIB::deal_socketmsg(TcpSocket *sock)
{
    string recv_msg = sock->recvSockmsg();
    // 首先判断认证类是否生成公私钥
    if (m_process != nullptr && m_process->is_fullkey)
    {
        std::cout << std::endl;
        std::cout << "====================Received AE Message====================" << std::endl;
        // 输出来端信息
        struct sockaddr_in peer_addr;
        socklen_t peer_addr_len = sizeof(peer_addr);
        if (getpeername(sock->getSocket(), (struct sockaddr *)&peer_addr, &peer_addr_len) == 0)
        {
            char peer_ip[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, &peer_addr.sin_addr, peer_ip, INET_ADDRSTRLEN);
            int peer_port = ntohs(peer_addr.sin_port);
            std::cout << "Connection from: " << peer_ip << ":" << peer_port << std::endl;
        }
    }
    else
    {
        const char *message = "key not generate";
        sock->sendSockmsg(message);
        cout << "key not generate" << endl;
        return;
    }
}
