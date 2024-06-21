#include "process_parifree.h"
#include "kgc_parifree.h"
int main()
{

    std::string entity_pid1 = "cc1b71a101a2091422315e52db4b61c5";
    std::string entity_wit1 = "209d974e66697397ea78cbaa9a81da805e837da10f993010f93f57b8f8098781b149015ff87dfb29b2a06b12612bc5c2a1825dc99805dccdaec0b8f5923b6a18";

    std::string entity_pid2 = "99bab9c0c59f0154f49b1b15c3d62257";
    std::string entity_wit2 = "a6ce2377bfc63b8232add83ec40cda7b49d553a5a28351317fc64e1bacc9aa65233a597ae0ffb2117e43d67e8418bfd651ccf975835b135ae3719b1cd0fef706";

    // std::string entity_pid3 = "6164916b3314f2ce4a3150e9173a5179";
    // std::string entity_wit3 = "57bcfebcde5b373a6d14916d50585f9f39152ff5bf95ab9f1ba5b7447a02112851b345c3ff6a0bc1fd9c404d3905e9b4eba68bcd6220d32d91929c6606a464c5";

    // std::string new_entity_pid = "64a57cc12951bd9a84b4a2ba12d51c79";

    std::string acc_publickey = "a775863f0ad44ca20035dbc8bee624ec9d65415f670e0a7b501bffb6bb298c064d977c6f3a43728ca6a4eca0c35cf0a3957c007de7b601e4302738a734c3bd43";
    std::string acc_cur = "39859795dc8efa3f73359ef8b259e7e39b48061a8abc00262ac8671187e7a7a7066d7813432534865f96d808087842ce12e5eb933dc52d286f581f6855d7d11b";
    std::string kgc_Ppub = "3db34e39a4c85d2d6e17dd25e8a08c42d349e791b509f6fcfe3e3daaf567a5ca603db34e39a4c85d2d6e17dd25e8a08c42d349e791b509f6fcfe3e3daaf567a5ca6";

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
}
