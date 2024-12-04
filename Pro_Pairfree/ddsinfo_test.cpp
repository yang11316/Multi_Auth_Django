#include "cls_lib.h"
using namespace std;

int main()
{
    CLS_LIB cls("0.0.0.0", 9989, 9988, "127.0.0.1", 9000);
    cls.init();
    string pid = cls.get_process_pid();

    dds_info info;
    info.dds_type = 1;
    info.protocol_type = 1;
    info.source_ip = "192.168.1.1";
    info.source_interface = "ens34";
    info.source_mask = "255.255.255.255";
    info.source_port = 9100;
    info.destination_ip = "192.168.1.1";
    info.destination_mac = "00:10:00:00:00:a4";
    info.destination_mask = "255.255.255.255";
    info.destination_port = 9120;
    if (cls.send_DDS_info(pid, info))
    {
        cout << "send success" << endl;
    }
    else
    {
        cout << "send failed" << endl;
    }

    return 0;
}