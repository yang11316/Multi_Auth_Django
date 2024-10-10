#include "comm_parifree.h"
int main(int argc, char *argv[])
{
    if (argc != 1)
    {
        std::cerr << "too much args" << std::endl;
        return 1;
    }

    std::string listening_ip = "0.0.0.0";
    unsigned short listening_port = std::stoi("9999");
    unsigned short sending_port = std::stoi("9998");
    std::string ap_ip = "127.0.0.1";
    unsigned short ap_port = std::stoi("9000");
    unsigned int processid = getpid();

    std::cout << "=====================malicious program=====================" << std::endl;
    std::cout << "====================setting information====================" << std::endl;
    std::cout << "entity_pid: " << processid << std::endl;
    std::cout << "Listening IP: " << listening_ip << ", Listening Port: " << listening_port << std::endl;
    std::cout << "AP IP: " << ap_ip << ", AP Port: " << ap_port << std::endl;
    std::cout << "===========================================================" << std::endl;

    std::thread listen_thread(linstening_connection, listening_port);
    send_http_msg(processid, ap_ip, ap_port, listening_port, sending_port, listening_ip);
    listen_thread.join();
    return 0;
}