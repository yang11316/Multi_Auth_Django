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
    int count = 1;
    while (count--)
    {
        int fd = server.acceptConn(0);
        if (fd < 0)
        {
            continue;
        }
        std::thread worker(worker_thread, fd, cls);
        worker.join();
    }
    server.closefd();
}

int main()
{
    // 使用封装的库函数
    CLS_LIB cls("0.0.0.0", 9929, 9928, "127.0.0.1", 9000);
    // 启动监听

    if (!cls.init())
    {
        cout << "init failed" << endl;
        return -1;
    }
    cout << "start listening" << endl;
    // cls.start();

    // 启动socket(测试用例)
    string sock_ip;
    unsigned short sock_port;
    cout << "inpout sending ip:" << endl;
    string send_ip;
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
        cout << "sign msg: " << signmsg << endl;
        TcpSocket sock;
        sock.connectToHost(send_ip, send_port);
        sock.sendMsg(signmsg, 0);
        sock.disConnect();
    }

    cout << "input listening ip:" << endl;
    cin >> sock_ip;

    cout << "input listening port:" << endl;
    cin >> sock_port;
    std::thread sock_thread(&server_listening, sock_ip, sock_port, &cls);
    cout << "listening...." << endl;
    // cls.stop();
    // cls.join();
    sock_thread.join();
    return 0;
}