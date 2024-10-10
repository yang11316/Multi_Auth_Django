#include "comm_utils.h"

using namespace boost::asio;
using boost::system::error_code;
using ip::tcp;

comm_utils::comm_utils(boost::asio::io_context &listening_io, std::string &listening_ip, unsigned short listening_port, unsigned short sending_port, std::string &local_ip) : _listening_io(listening_io), _m_acceptor(listening_io, tcp::endpoint(address::from_string(listening_ip), listening_port))
{
    this->_listening_port = listening_port;
    this->_sending_port = sending_port;
    this->_local_ip = local_ip;
}
void comm_utils::start_listening()
{
    // 开始等待连接（非阻塞）
    boost::shared_ptr<tcp::socket> psocket(new tcp::socket(_listening_io));
    // 触发的事件只有error_code参数，所以用boost::bind把socket绑定进去
    _m_acceptor.async_accept(*psocket,
                             boost::bind(&comm_utils::accept_handler, this, psocket, _1));
}
void comm_utils::accept_handler(boost::shared_ptr<tcp::socket> psocket, error_code ec)
{
    if (ec)
        return;
    // 继续等待连接
    start_listening();
    // 发送信息(非阻塞)
    std::vector<char> buf(2048);

    size_t len = psocket->receive(buffer(buf));
    // 读取全部报文
    try
    {
        std::string request_msg(buf.data(), len);
        if (request_msg.find("POST /") == 0)
        {
            // HTTP POST 请求
            deal_httpmsg(request_msg, psocket);
        }
        else
        {
            deal_socketmsg(request_msg, psocket);
        }
    }
    catch (const std::exception &e)
    {
        std::cerr << e.what() << '\n';
    }
}
void comm_utils::write_handler(boost::shared_ptr<std::string> pstr,
                               error_code ec, size_t bytes_transferred)
{
    if (ec)
        std::cout << "发送失败!" << std::endl;
    else
        std::cout << *pstr << " 已发送" << std::endl;
}
std::unordered_map<std::string, std::string> comm_utils::parse_form_data(const std::string &request)
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

void comm_utils::deal_socketmsg(std::string &request_msg, boost::shared_ptr<tcp::socket> psocket)
{
    std::cout << "Receive socket msg from" << psocket->remote_endpoint().address().to_string() << std::endl;
    std::unordered_map<std::string, std::string> payload_map = parse_form_data(request_msg);
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

    if (this->process->verify_sign(recv_payload))
    {
        boost::shared_ptr<std::string> pstr(new std::string("sucess"));
        psocket->async_write_some(buffer(*pstr),
                                  boost::bind(&comm_utils::write_handler, this, pstr, _1, _2));
    }
    else
    {
        boost::shared_ptr<std::string> pstr(new std::string("fail"));
        psocket->async_write_some(buffer(*pstr),
                                  boost::bind(&comm_utils::write_handler, this, pstr, _1, _2));
    }
}
void comm_utils::deal_httpmsg(std::string &request_msg, boost::shared_ptr<tcp::socket> psocket)
{
    std::unordered_map<std::string, std::string>
        params = parse_form_data(request_msg);
    // 输出解析结果
    std::cout << "Received HTTP parameters:" << std::endl;
    std::cout << params.size() << " parameters" << std::endl;
    for (const auto &pair : params)
    {
        std::cout << pair.first << ": " << pair.second << std::endl;
    }
    std::cout << "receive end" << std::endl;

    // 如果长度是1则为发布的aux消息
    if (params.size() == 1)
    {
        this->process->update_key(params["aux"]);
    }
    else if (params.size() == 4)
    {
        if (this->process != nullptr)
        {
            this->process->acc_cur = mpz_class(params["acc_cur"], 16);
            this->process->pid = params["pid"];
            this->process->acc_publickey = mpz_class(params["acc_publickey"], 16);
            this->process->Pub = crypto_utils::hex2point(this->process->ec_group, params["Pub"]);
        }
        else
        {
            this->process = new Process(params["pid"], params["acc_publickey"], params["acc_cur"], params["kgc_Ppub"]);
        }
    }
    else if (params.size() == 5)
    {
        if (this->process != nullptr)
        {
            this->process->acc_cur = mpz_class(params["acc_cur"], 16);
            this->process->pid = params["pid"];
            this->process->acc_publickey = mpz_class(params["acc_publickey"], 16);
            this->process->Pub = crypto_utils::hex2point(this->process->ec_group, params["Pub"]);
            this->process->acc_witness = mpz_class(params["acc_witness"], 16);
            this->process->generate_full_key();
        }
        else
        {
            this->process = new Process(params["pid"], params["acc_publickey"], params["acc_cur"], params["entity_parcialkey"], params["kgc_Ppub"]);
        }
    }
    // 返回 HTTP 响应
    boost::shared_ptr<std::string> pstr(new std::string("HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nok"));
    psocket->async_write_some(buffer(*pstr),
                              boost::bind(&comm_utils::write_handler, this, pstr, _1, _2));
}

void comm_utils::send_http_to_AP(boost::asio::io_context &sending_io, std::string &sending_ip, unsigned short sending_port, std::string &entity_pid)
{

    tcp::endpoint tmp_endpoint(tcp::v4(), this->_sending_port);
    tcp::socket tmp_socket(sending_io, tmp_endpoint);
    tmp_socket.connect(tcp::endpoint(boost::asio::ip::address::from_string(sending_ip), sending_port));
    std::string local_ip = tmp_socket.local_endpoint().address().to_string();
    std::cout << "send http to AP, local ip:" << local_ip << std::endl;
    std::string post_data = "entity_pid=" + entity_pid + "&port=" + std::to_string(this->_listening_port) + "&";
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

    // 发送 HTTP 请求
    boost::asio::write(tmp_socket, boost::asio::buffer(post_request));
    tmp_socket.close();
}

void comm_utils::send_sinature_to_process(boost::asio::io_context &sending_io, std::string &sending_ip, unsigned short sending_port, std::string &msg)
{
    try
    {
        std::cout << this->_sending_port << std::endl;
        tcp::endpoint tmp_endpoint(tcp::v4(), this->_sending_port);
        tcp::socket tmp_socket(sending_io);

        std::cout << this->process->acc_publickey.get_str(16) << std::endl;
        sign_payload payload = this->process->sign(msg);
        std::string socket_data = payload.to_string();
        std::cout << "send signature to process" << std::endl;
        tmp_socket.connect(tcp::endpoint(boost::asio::ip::address::from_string(sending_ip), sending_port));
        boost::asio::write(tmp_socket, boost::asio::buffer(socket_data));
        // 读取响应
        boost::asio::streambuf response;
        boost::asio::read(tmp_socket, response);
        // 输出响应
        std::cout << "Response from server:\n";
        std::cout << &response;
        tmp_socket.close();
    }
    catch (const std::exception &e)
    {
        std::cerr << e.what() << '\n';
    }
}