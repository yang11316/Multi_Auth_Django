#include "process_parifree.h"
#include "kgc_parifree.h"
int main()
{

    std::string entity_pid1 = "f074b296668195b44f917aed12735ca7";
    std::string entity_wit1 = "1d330c57740031a9ccf54a19e51ce0b8d55ceaff63e9f125729065039865e2a6ffb7ae6b21c98aa62bd72e1673981a66b87229d6d85d8e3b4c38cf09dda01697";

    std::string entity_pid2 = "25fe99e5d61f0a599fa9cece1b5120af";
    std::string entity_wit2 = "22fa24c9d5fecbe3d565bdaad993093a680ca1547b89682a5c5c610ec6fe1fa8bb1118bb3be2cc182ca38df0d703a4138facdff56a084b5391ddd088341d5f79";

    std::string entity_pid3 = "6164916b3314f2ce4a3150e9173a5179";
    std::string entity_wit3 = "57bcfebcde5b373a6d14916d50585f9f39152ff5bf95ab9f1ba5b7447a02112851b345c3ff6a0bc1fd9c404d3905e9b4eba68bcd6220d32d91929c6606a464c5";

    std::string new_entity_pid = "64a57cc12951bd9a84b4a2ba12d51c79";

    std::string acc_publickey = "a775863f0ad44ca20035dbc8bee624ec9d65415f670e0a7b501bffb6bb298c064d977c6f3a43728ca6a4eca0c35cf0a3957c007de7b601e4302738a734c3bd43";
    std::string acc_cur = "1ab142e1c8f405d4372da735ff0e3ff5b838e05bef312e46002778c6dc3a90ea05aac553711a2a3e5227eba760f530b8fa0aaa53f29208eb2b0caf82a37a53c8";
    std::string kgc_Ppub = "03db34e39a4c85d2d6e17dd25e8a08c42d349e791b509f6fcfe3e3daaf567a5ca6";

    // KGC *kgc = new KGC(NID_secp256k1);
    // std::cout << "kgc_q:" << kgc->get_q() << std::endl;
    // std::cout << "kgc_Ppub:" << kgc->get_Ppub() << std::endl;

    Process *p1 = new Process(entity_pid1, acc_publickey, acc_cur, entity_wit1, kgc_Ppub);
    // std::cout << "p1_q:" << crypto_utils::bn2hex(p1->q) << std::endl;
    // std::cout << "p1_curve:" << EC_CURVE(p1->ec_group) << std::endl;

    Process *p2 = new Process(entity_pid2, acc_publickey, acc_cur, entity_wit2, kgc_Ppub);
    // std::cout << "p2_q:" << crypto_utils::bn2hex(p2->q) << std::endl;

    // Process *p3 = new Process(entity_pid3, acc_publickey, acc_cur, entity_wit3, kgc_Ppub);

    std::string msg = "hello";
    p1->generate_full_key();
    // p1->update_key(new_entity_pid);
    p2->generate_full_key();
    // p2->update_key(new_entity_pid);

    std::cout << crypto_utils::point2hex(p1->ec_group, p1->WIT) << std::endl;
    sign_payload payload = p1->sign(msg);
    if (p2->verify_sign(payload))
    {
        std::cout << "msg verify sucessfully" << std::endl;
    }
    else
    {
        std::cout << "msg verify failed" << std::endl;
    }

    /*

    payload.wit_hex = "6ba8fc8c7facd4ef3a2659ee926dc3d24fd08d1b517d8547190295c34879ded7892c9e6ac854053282b81980d9cdf2f9d5ef6019f9db723a384a02e651dadf58ea1b822b6e48ccc041d26db1845ef7cc652cebe808fc551fd94a03069511771bd68f40fc9a5ec2de1761882610101f5370cc14f09df6d5bf0dd2c07b206f5ad1";
    payload.WIT = "02103FCB47650EDF1E68DA1A04C3E7FBA73D3C32A4ECAE5DB746A49DE5FBAC0996";
    payload.X = "0264e1b1969f9102977691a40431b0b672055dcf31163897d996434420e6c95dc9";
    payload.time_stamp = "1713174266887";
    payload.sig2 = "0c1bc8118bbd17799c08078255b5e78c100943ce6a4ee22a6d9d6a8229dd05a9";
    payload.sig1 = "0278fb5a971c97d58e8c314fed04873387cd56c7f2803b45cc3363ad7a3cdde20c";
    payload.msg = "hello";
    payload.pid = "f074b296668195b44f917aed12735ca7";

    if (p2->verify_sign(payload))
    {
        std::cout << "msg verify sucessfully" << std::endl;
    }
    else
    {
        std::cout << "msg verify failed" << std::endl;
    }
    */
}
