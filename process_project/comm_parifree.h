#include "process_parifree.h"
#include <iostream>
#include <thread>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unordered_map>
#include <sys/time.h>

constexpr int MAX_BUFFER_SIZE = 2048;
constexpr int BACKLOG = 10;
Process process;
// 解析传来的参数 格式：a=b&c=bbb
std::unordered_map<std::string, std::string> parse_form_data(const std::string &request)
{
    std::unordered_map<std::string, std::string> result;
    size_t pos = request.find("\r\n\r\n");
    std::cout << pos << std::endl;
    if (pos != std::string::npos)
    {
        // 获取json格式数据
        std::string data = request.substr(pos + 4);
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
                // 这里省略了 URL 解码的步骤，你可以根据需要实现

                // 存储键值对
                result[key] = value;
            }
            pos = end_pos + 1;
        }
    }

    return result;
}
std::unordered_map<std::string, std::string> parse_form_data_process(const std::string &data)
{

    std::unordered_map<std::string, std::string> result;
    // 获取json格式数据
    // 按 '&' 分割数据
    int pos = 0;
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
            // 这里省略了 URL 解码的步骤，你可以根据需要实现

            // 存储键值对
            result[key] = value;
        }
        pos = end_pos + 1;
    }

    return result;
}
bool socket_send(const std::string &message, const std::string &send_ip, const unsigned short send_port, const unsigned short sending_port)
{
    struct sockaddr_in serv_addr;
    // 创建 socket 文件描述符
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1)
    {
        std::cerr << "send sign msg socket creation error" << std::endl;
        return false;
    }

    // 设置允许地址端口复用
    int opt = 1;
    if (setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, (const void *)&opt, sizeof(opt)) < 0)
    {
        std::cerr << "Error setting reuseaddr: " << std::strerror(errno) << std::endl;
        return false;
    }

    // 设置超时时间为5秒
    struct timeval timeout;
    timeout.tv_sec = 5; // 5秒
    timeout.tv_usec = 0;
    if (setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, (char *)&timeout, sizeof(timeout)) < 0)
    {
        std::cerr << "Error setting receive timeout: " << std::strerror(errno) << std::endl;
        return false;
    }

    // 设置本地地址和端口号
    struct sockaddr_in local_addr;
    memset(&local_addr, '0', sizeof(local_addr));
    local_addr.sin_family = AF_INET;
    local_addr.sin_addr.s_addr = htonl(INADDR_ANY); // 本地地址
    local_addr.sin_port = htons(sending_port);      // 绑定的端口号

    // 绑定 socket 到本地地址和端口
    if (bind(sock, (struct sockaddr *)&local_addr, sizeof(local_addr)) < 0)
    {
        std::cerr << "Bind failed" << std::endl;
        return false;
    }

    // 设置要发送到的端口号
    memset(&serv_addr, '0', sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(send_port);

    // 将IP地址从点分十进制转换为网络字节序
    if (inet_pton(AF_INET, send_ip.data(), &serv_addr.sin_addr) <= 0)
    {
        std::cerr << "Invalid address/ Address not supported" << std::endl;
        return false;
    }

    // 连接到服务器
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        std::cerr << "Connection Failed" << std::endl;
        return false;
    }

    if (send(sock, message.data(), strlen(message.data()), 0) != strlen(message.data()))
    {
        std::cerr << "Send failed" << std::endl;
        return false;
    }
    // std::cout << strlen(message.data()) << std::endl;
    std::cout << "Message sent" << std::endl;

    // 读取服务器返回的数据
    std::vector<char> buffer(MAX_BUFFER_SIZE);
    ssize_t valread = recv(sock, buffer.data(), buffer.size(), 0);
    if (valread < 0)
    {
        std::cerr << "Recv failed" << std::endl;
        return false;
    }
    std::cout << "Server response: " << buffer.data() << std::endl;
    close(sock);
    return true;
}

void deal_httpmsg(std::string &recv_data, int client_socket)
{
    std::unordered_map<std::string, std::string>
        params = parse_form_data(recv_data);
    // 输出解析结果
    std::cout << "====================Received AP Message====================" << std::endl;
    std::cout << params.size() << " parameters:" << std::endl;
    for (const auto &pair : params)
    {
        std::cout << pair.first << ": " << pair.second << std::endl;
    }
    // 如果长度是1则为发布的aux消息
    if (params.size() == 1)
    {
        process.update_key(params["aux"]);
        std::cout << "partical key update" << std::endl;
        std::cout << "accumulator:" << process.acc_cur.get_str(16) << std::endl;
    }
    else if (params.size() == 4)
    {
        if (process.is_init)
        {
            process.acc_cur = mpz_class(params["acc_cur"], 16);
            process.pid = params["pid"];
            process.acc_publickey = mpz_class(params["acc_publickey"], 16);
            process.Pub = crypto_utils::hex2point(process.ec_group, params["Pub"]);
        }
        else
        {
            process.init(params["pid"], params["acc_publickey"], params["acc_cur"], params["kgc_Ppub"]);
        }
    }
    else if (params.size() == 5)
    {
        if (process.is_init)
        {
            process.acc_cur = mpz_class(params["acc_cur"], 16);
            process.pid = params["pid"];
            process.acc_publickey = mpz_class(params["acc_publickey"], 16);
            process.Pub = crypto_utils::hex2point(process.ec_group, params["Pub"]);
            process.acc_witness = mpz_class(params["acc_witness"], 16);

            // 测量密钥生成时间
            if (process.generate_full_key())
            {
                std::cout << "generate full key sucess" << std::endl;
            }
            else
            {
                std::cout << "generate full key error" << std::endl;
            }
        }
        else
        {
            process.init(params["pid"], params["acc_publickey"], params["acc_cur"], params["entity_parcialkey"], params["kgc_Ppub"]);
            process.generate_full_key();
        }
    }
    std::cout << "===========================================================" << std::endl;
    const char *response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n";
    send(client_socket, response, strlen(response), 0);
}
void deal_socketmsg(std::string &recv_data, int client_socket)
{
    if (process.is_fullkey)
    {
        // 输出来端信息
        struct sockaddr_in peer_addr;
        socklen_t peer_addr_len = sizeof(peer_addr);
        std::cout << std::endl;
        std::cout << "====================Received AE Message====================" << std::endl;
        if (getpeername(client_socket, (struct sockaddr *)&peer_addr, &peer_addr_len) == 0)
        {
            char peer_ip[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, &peer_addr.sin_addr, peer_ip, INET_ADDRSTRLEN);
            int peer_port = ntohs(peer_addr.sin_port);

            std::cout << "Connection from: " << peer_ip << ":" << peer_port << std::endl;
        }

        std::unordered_map<std::string, std::string> payload_map = parse_form_data_process(recv_data);
        std::cout << payload_map.size() << "payload parameters" << std::endl;
        for (const auto &pair : payload_map)
        {
            std::cout << pair.first << ": " << pair.second << std::endl;
        }
        sign_payload recv_payload;
        recv_payload.pid = payload_map["pid"];
        recv_payload.msg = payload_map["msg"];
        recv_payload.sig1 = payload_map["sig1"];
        recv_payload.sig2 = payload_map["sig2"];
        recv_payload.time_stamp = payload_map["time_stamp"];
        recv_payload.WIT = payload_map["WIT"];
        recv_payload.wit_hex = payload_map["wit_hex"];
        recv_payload.X = payload_map["X"];

        if (process.verify_sign(recv_payload))
        {
            std::cout << "verify success, message: " << recv_payload.msg << std::endl;
            const char *message = "verify success";
            send(client_socket, message, strlen(message), 0);
        }
        else
        {
            const char *message = "verify failed";
            send(client_socket, message, strlen(message), 0);
        }

        std::cout << "=======================================================" << std::endl;
    }
    else
    {
        const char *message = "key not generate";
        send(client_socket, message, strlen(message), 0);
    }
}
void handle_client(int client_socket)
{
    std::vector<char> buffer(MAX_BUFFER_SIZE);
    // 接收数据
    ssize_t bytes_received = recv(client_socket, buffer.data(), buffer.size(), 0);
    if (bytes_received == -1)
    {
        std::cerr << "Error: Failed to receive data from client." << std::endl;
        close(client_socket);
        return;
    }

    std::string recv_data(buffer.data(), bytes_received);
    // 输出接收到的数据
    // std::cout << "====================Received data from client====================" << std::endl;
    // std::cout << recv_data << std::endl;
    // std::cout << "================================================================" << std::endl;

    if (recv_data.find("POST /") == 0)
    {
        // HTTP POST 请求
        deal_httpmsg(recv_data, client_socket);
    }
    else
    {
        deal_socketmsg(recv_data, client_socket);
    }

    // 关闭套接字
    close(client_socket);
}
void linstening_connection(int listening_port)
{
    // 创建套接字
    int server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket == -1)
    {
        std::cerr << "Error: Failed to create socket." << std::endl;
        return;
    }

    // 准备地址结构体
    sockaddr_in server_addr;
    std::memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    // 监听所有网络接口
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(listening_port);
    // 绑定地址
    if (bind(server_socket, reinterpret_cast<sockaddr *>(&server_addr), sizeof(server_addr)) == -1)
    {
        std::cerr << "Error: Failed to bind socket to port " << listening_port << "." << std::endl;
        close(server_socket);
        return;
    }
    // 监听连接
    if (listen(server_socket, BACKLOG) == -1)
    {
        std::cerr << "Error: Failed to listen on socket." << std::endl;
        close(server_socket);
        return;
    }
    while (true)
    {
        // 接收连接
        sockaddr_in client_addr;
        socklen_t client_addr_len = sizeof(client_addr);
        int client_socket = accept(server_socket, reinterpret_cast<sockaddr *>(&client_addr), &client_addr_len);
        if (client_socket == -1)
        {
            std::cerr << "Error: Failed to accept connection." << std::endl;
            continue;
        }

        // 创建新的线程来处理客户端连接
        std::thread client_thread(handle_client, client_socket);

        // struct timeval begtime, endtime;
        // gettimeofday(&begtime, NULL);
        // std::cout << "===== 开始计算耗时 =====" << std::endl;
        client_thread.join();
        // gettimeofday(&endtime, NULL);
        // long timeuse = 1000000 * (endtime.tv_sec - begtime.tv_sec) + endtime.tv_usec - begtime.tv_usec;
        // printf("互认证耗时: %ld us\n", timeuse);
    }
}

void send_sign_msg(const std::string &msg, const std::string &send_ip, const unsigned short send_port, const unsigned short sending_port)
{
    // std::cout << process.acc_publickey.get_str(16) << std::endl;
    std::cout << std::endl;
    std::cout << "====================Send Sign Message====================" << std::endl;
    if (!process.is_fullkey)
    {
        std::cout << "error: not generate full key" << std::endl;
        return;
    }
    // 对消息进行签名
    sign_payload payload = process.sign(msg);
    std::cout << payload.to_string() << std::endl;
    std::string msg_str = "pid=" + payload.pid + "&msg=" + payload.msg + "&sig1=" + payload.sig1 + "&sig2=" + payload.sig2 + "&time_stamp=" + payload.time_stamp + "&WIT=" + payload.WIT + "&wit_hex=" + payload.wit_hex + "&X=" + payload.X;
    const char *message = msg_str.c_str();
    if (socket_send(message, send_ip, send_port, sending_port))
    {
        std::cout << "send message: " << message << std::endl;
        std::cout << "send sign message success" << std::endl;
    }
    else
    {
        std::cout << "send fail" << std::endl;
    }
    std::cout << "=======================================================" << std::endl;
    return;
}

void send_http_msg(const int processid, const std::string &send_ip, const unsigned short send_port, const unsigned short listening_port, const unsigned short sending_port, const std::string &local_ip)
{
    std::cout << std::endl;
    std::cout << "====================Send HTTP Message====================" << std::endl;
    std::string post_data = "processid=" + std::to_string(processid) + "&listening_port=" + std::to_string(listening_port) + "&sending_port=" + std::to_string(sending_port);
    std::string post_request =
        "POST /entitymanage/sendparticalkeyandpid/ HTTP/1.1\r\n"
        "Host: " +
        local_ip +
        "\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: " +
        std::to_string(post_data.size()) + "\r\n"
                                           "\r\n" +
        post_data;
    // std::cout << post_request << std::endl;
    const char *message = post_request.c_str();
    if (socket_send(message, send_ip, send_port, sending_port))
    {
        std::cout << "parameters request http message send success" << std::endl;
    }
    else
    {
        std::cout << "parameters request http message send fail" << std::endl;
    }
    std::cout << "=======================================================" << std::endl;
    return;
}

// 获取当前进程PID
pid_t get_current_pid()
{
    return getpid();
}