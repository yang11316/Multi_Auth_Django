#include <iostream>
#include <string>
#include <boost/asio.hpp>

using boost::asio::ip::tcp;

int main()
{
    try
    {
        // 初始化 Boost 库的 IO 服务
        boost::asio::io_service io_service;
        // 创建 Socket
        tcp::socket socket(io_service);
        // 连接到服务器
        socket.connect(tcp::endpoint(boost::asio::ip::address::from_string("192.168.3.17"), 9999));

        std::string post_data = "kgc_q=FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141&kgc_acc_G=97ef1f09dcc6e81e2c08f3c96f04710fe1d05b39ac00e6fc190de20293c7ee01&kgc_acc_publickey=a775863f0ad44ca20035dbc8bee624ec9d65415f670e0a7b501bffb6bb298c064d977c6f3a43728ca6a4eca0c35cf0a3957c007de7b601e4302738a734c3bd43&kgc_acc_cur=1ab142e1c8f405d4372da735ff0e3ff5b838e05bef312e46002778c6dc3a90ea05aac553711a2a3e5227eba760f530b8fa0aaa53f29208eb2b0caf82a37a53c8&kgc_ppub=555573397600871564240997220663272622824235127397015844622771194939726420902553690405072832038755241919812755601638224280272977625777698193749598354118710";
        // 构造 HTTP POST 请求
        std::string post_request =
            "POST /your-endpoint HTTP/1.1\r\n"
            "Host: your-hostname\r\n"
            "Content-Type: application/json\r\n"
            "Content-Length: " +
            std::to_string(post_data.size()) + "\r\n"
                                               "\r\n" +
            post_data;

        // 发送 HTTP 请求
        boost::asio::write(socket, boost::asio::buffer(post_request));

        // 接收服务器的响应
        boost::asio::streambuf response;
        boost::asio::read(socket, response);
        // 输出响应
        std::cout << "Response from server:\n";
        std::cout << &response;
        socket.close();
    }
    catch (std::exception &e)
    {
        std::cerr << "Exception: " << e.what() << std::endl;
    }
    return 0;
}
