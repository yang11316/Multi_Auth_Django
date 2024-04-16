#include <iostream>
#include <boost/asio.hpp>
#include <unordered_map>
#include <string>

using namespace boost::asio;
using namespace boost::asio::ip;

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

int main()
{
    io_context service;
    ip::tcp::acceptor acceptor(service, ip::tcp::endpoint(boost::asio::ip::address::from_string("0.0.0.0"), 9999));

    while (true)
    {
        ip::tcp::socket socket(service);
        acceptor.accept(socket);

        // 读取请求类型
        std::vector<char> buf(1024);

        size_t len = socket.receive(boost::asio::buffer(buf));
        // 读取全部报文
        std::string requestType(buf.data(), len);
        if (requestType.find("POST /") == 0)
        {
            // HTTP POST 请求
            std::string data(buf.begin(), buf.end());
            std::unordered_map<std::string, std::string>
                params = parse_form_data(data);
            // 输出解析结果
            std::cout << "Received HTTP parameters:" << std::endl;
            std::cout << params.size() << " parameters" << std::endl;
            for (const auto &pair : params)
            {
                std::cout << pair.first << ": " << pair.second << std::endl;
            }
            std::cout << "receive end" << std::endl;
            // 返回 HTTP 响应
            std::string response = "HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nok";
            write(socket, buffer(response));
        }
        else
        {
            // Socket 请求
            std::string requestData(buf.data(), len);
            std::cout << "Received Socket request: " << requestData << std::endl;

            // 返回 Socket 响应
            std::string response = "Response from Socket server";
            write(socket, buffer(response + "\n"));
        }
    }

    return 0;
}
