#include "cls_lib.h"
using namespace std;

int main()
{
    CLS_LIB cls("0.0.0.0", 9999, 9998, "127.0.0.1", 9000);
    // vector<uint16_t> vec{999, 123};
    // bool ret = cls.open_port(vec);
    if (cls.init())
    {
        string msg = "hello world";
        cout << cls.get_key_size() << endl;

        string sig = cls.sign(msg);
        cout << sig << endl;
        string sig2 = cls.sign(msg);
        cout << sig2 << endl;

        string sig3 = cls.sign(msg);
        cout << sig3 << endl;

        string sig4 = cls.sign(msg);
        cout << sig4 << endl;

        cls.delete_key("e05b4c63915826d59a850dccafd5e64d");
        cout << cls.get_key_size() << endl;
        cls.delete_key("e05b4c63915826d59a850dccafd5e64d");
    }
}