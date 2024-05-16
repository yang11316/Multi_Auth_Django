#include "comm_parifree.h"

int main(int argc, char *argv[])
{
    // 检查命令行参数数量
    if (argc != 9)
    {
        std::cerr << "Usage: " << argv[0] << " <message> <listening_ip> <listening_port> <sending_port> <send_ip> <send_port> <ap_ip> <ap_port>" << std::endl;
        return 1;
    }
    // 从命令行参数中获取信息
    std::string message = argv[1];
    std::string listening_ip = argv[2];
    unsigned short listening_port = std::stoi(argv[3]);
    unsigned short sending_port = std::stoi(argv[4]);
    std::string send_ip = argv[5];
    unsigned short send_port = std::stoi(argv[6]);
    std::string ap_ip = argv[7];
    unsigned short ap_port = std::stoi(argv[8]);
    unsigned int processid = getpid();
    // 输出获取到的信息
    std::cout << "entity_pid: " << processid << std::endl;
    std::cout << "Listening IP: " << listening_ip << ", Listening Port: " << listening_port << std::endl;
    std::cout << "Sending IP: " << send_ip << ", Sending Port: " << send_port << std::endl;
    std::cout << "AP IP: " << ap_ip << ", AP Port: " << ap_port << std::endl;

    // 开启循环监听
    std::thread listen_thread(linstening_connection, listening_port);
    send_http_msg(processid, ap_ip, ap_port, listening_port, sending_port, listening_ip);
    if (send_ip.compare("0"))
    {
        sleep(3);
        send_sign_msg(message, send_ip, send_port, sending_port);
    }
    listen_thread.join();

    return 0;
}