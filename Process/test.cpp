#include "process_parifree.h"
#include "kgc_parifree.h"
#include <gmp.h>
int main()
{

    std::string entity_pid1 = "8d4fc294692977119560d72077f898cf";
    std::string entity_wit1 = "a0bec37f018ead7be73dbf6319b4da0720145217c7465a5da7f9b5ef301042c11de40c7b5bd461c3151bf5bb4f6f78154390d5ed47f706ca42cff90f9df8640";

    std::string entity_pid2 = "e0ce7741de1aac5d2001cf69f03c1f5b";
    std::string entity_wit2 = "9b2a76d0f55f0aedc24770de41d98354956c8e3521483997f7202586d915a53a2c83e7f3c98898078404084aa54aa055a6e34eef9fa0b9693706da8295aca56d";

    // std::string entity_pid3 = "6164916b3314f2ce4a3150e9173a5179";
    // std::string entity_wit3 = "57bcfebcde5b373a6d14916d50585f9f39152ff5bf95ab9f1ba5b7447a02112851b345c3ff6a0bc1fd9c404d3905e9b4eba68bcd6220d32d91929c6606a464c5";

    // std::string new_entity_pid = "64a57cc12951bd9a84b4a2ba12d51c79";

    std::string acc_publickey = "a775863f0ad44ca20035dbc8bee624ec9d65415f670e0a7b501bffb6bb298c064d977c6f3a43728ca6a4eca0c35cf0a3957c007de7b601e4302738a734c3bd43";
    std::string acc_cur = "34afc84666ecfd41558e7333606d3276b81d6d9790a7f0cc13bae3fc2c5b9febef724cae3d1b3d2687a522ba0473aafdd4c39d39dc9fbdad38e4f1bcd09ffa7c";
    std::string kgc_Ppub = "558368450755296179496037359485219377540353696815398107360446924983611510369895163653151980645886045235543017750949559947961392591210629752287725973442146";

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
