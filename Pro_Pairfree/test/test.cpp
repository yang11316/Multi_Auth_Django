#include "cls_lib.h"
using namespace std;
void worker_thread(int fd, CLS_LIB *cls)
{
    TcpSocket tmp_sock(fd);
    string msg = tmp_sock.recvmsg(0, 0);
    cout << "recv msg: " << msg << endl;
    if (cls->verify(msg))
    {
        cout << "verify success" << endl;
    }
    else
    {
        cout << "verify failed" << endl;
    }
}
void server_listening(string ip, unsigned short port, CLS_LIB *cls)
{
    TcpServer server(ip, port);
    int ret = server.setListen();
    while (1)
    {
        int fd = server.acceptConn(0);
        if (fd < 0)
        {
            continue;
        }
        std::thread worker(worker_thread, fd, cls);
        worker.join();
    }
}

int main()
{
    // 使用封装的库函数
    CLS_LIB cls("setting.json");
    // 启动监听
    cout << "start listening" << endl;
    std::thread start_thread(&CLS_LIB::startListening, &cls);
    cout << cls.init() << endl;

    // 启动socket(测试用例)
    string sock_ip;
    unsigned short sock_port;
    cout << "input listening ip:" << endl;
    cin >> sock_ip;
    cout << "input listening port:" << endl;
    cin >> sock_port;
    std::thread sock_thread(&server_listening, sock_ip, sock_port, &cls);
    cout << "listening...." << endl;

    string send_ip;

    cout << "inpout sending ip:" << endl;
    cin >> send_ip;
    if (send_ip != "0")
    {
        unsigned short send_port;
        cout << "input sending port:" << endl;
        cin >> send_port;
        string msg;
        cout << "input msg:" << endl;
        cin >> msg;
        string signmsg = cls.sign(msg);
        TcpSocket sock;
        sock.connectToHost(send_ip, send_port);
        sock.sendMsg(signmsg, 0);
        sock.disConnect();
    }

    sock_thread.join();
    start_thread.join();
    return 0;
}