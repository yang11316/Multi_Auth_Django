#include <iostream>
#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <unordered_map>
#include <string>
#include "process_parifree.h"
using namespace boost::asio;
using namespace boost::asio::ip;
using namespace boost::system;
class comm_utils
{
public:
    Process *process = nullptr;

    comm_utils(boost::asio::io_context &listening_io, std::string &listening_ip, unsigned short listening_port, unsigned short sending_port, std::string &local_ip);
    void send_http_to_AP(boost::asio::io_context &sending_io, std::string &sending_ip, unsigned short sending_port, std::string &entity_pid);
    void send_sinature_to_process(boost::asio::io_context &sending_io, std::string &sending_ip, unsigned short sending_port, std::string &msg);
    void start_listening();
    void accept_handler(boost::shared_ptr<tcp::socket> psocket, error_code ec);
    void write_handler(boost::shared_ptr<std::string> pstr,
                       error_code ec, size_t bytes_transferred);
    void deal_socketmsg(std::string &request_msg, boost::shared_ptr<tcp::socket> psocket);
    void deal_httpmsg(std::string &request_msg, boost::shared_ptr<tcp::socket> psocket);
    std::unordered_map<std::string, std::string> parse_form_data(const std::string &request);
    // void send_data(std::string &sending_ip, unsigned short sending_port, const std::string &data);

private:
    io_context &_listening_io;
    tcp::acceptor _m_acceptor;
    unsigned short _listening_port;
    unsigned short _sending_port;
    std::string _local_ip;

    // tcp::socket _m_lsocket;
};
