#include "process_parifree.h"
#include "kgc_parifree.h"
int main()
{

    std::string entity_pid1 = "f074b296668195b44f917aed12735ca7";
    std::string entity_wit1 = "1d330c57740031a9ccf54a19e51ce0b8d55ceaff63e9f125729065039865e2a6ffb7ae6b21c98aa62bd72e1673981a66b87229d6d85d8e3b4c38cf09dda01697";

    std::string entity_pid2 = "25fe99e5d61f0a599fa9cece1b5120af";
    std::string entity_wit2 = "22fa24c9d5fecbe3d565bdaad993093a680ca1547b89682a5c5c610ec6fe1fa8bb1118bb3be2cc182ca38df0d703a4138facdff56a084b5391ddd088341d5f79";

    std::string acc_publickey = "a775863f0ad44ca20035dbc8bee624ec9d65415f670e0a7b501bffb6bb298c064d977c6f3a43728ca6a4eca0c35cf0a3957c007de7b601e4302738a734c3bd43";
    std::string acc_cur = "1ab142e1c8f405d4372da735ff0e3ff5b838e05bef312e46002778c6dc3a90ea05aac553711a2a3e5227eba760f530b8fa0aaa53f29208eb2b0caf82a37a53c8";
    std::string kgc_q = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141";
    std::string kgc_Ppub = "03C939815CD24551A87C45A8DD9BC9B04324000933A4A8DD4B2BBBFEC4469B7F2A";

    // KGC *kgc = new KGC(NID_secp256k1);
    // std::cout << "kgc_q:" << kgc->get_q() << std::endl;
    // std::cout << "kgc_Ppub:" << kgc->get_Ppub() << std::endl;

    Process *p1 = new Process(entity_pid1, acc_publickey, acc_cur, entity_wit1, kgc_Ppub);
    std::cout << "p1_q:" << crypto_utils::bn2hex(p1->q) << std::endl;

    Process *p2 = new Process(entity_pid2, acc_publickey, acc_cur, entity_wit2, kgc_Ppub);
    std::cout << "p2_q:" << crypto_utils::bn2hex(p2->q) << std::endl;

    std::string msg = "hello!";
    p1->generate_full_key();
    std::cout << crypto_utils::point2hex(p1->ec_group, std::get<0>(p1->public_key)) << std::endl;
    sign_payload payload = p1->sign(msg);
    std::cout << "msg payload by p1:" << payload.sig2 << std::endl;
    payload.X = "1d330c57740031a9ccf54a19e51ce0b8d55ceaff63e9f12";
    if (p2->verify_sign(payload))
    {
        std::cout << "msg verify sucessfully" << std::endl;
    }
    else
    {
        std::cout << "msg verify failed" << std::endl;
    }
}