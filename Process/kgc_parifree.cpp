#include "kgc_parifree.h"

/// Initialize function
KGC::KGC(int nid)
{
    this->ec_group = EC_GROUP_new_by_curve_name(nid);
    // const EC_POINT *P = EC_GROUP_get0_generator(ec_group);
    const BIGNUM *order = EC_GROUP_get0_order(ec_group);

    this->q = BN_dup(order);
    this->s = BN_new();
    BN_rand_range(s, q);
    this->Pub = EC_POINT_new(ec_group);
    EC_POINT_mul(ec_group, Pub, s, nullptr, nullptr, nullptr);
}

KGC::KGC(const std::string &kgc_s, const std::string &kgc_q, int nid)
{
    this->ec_group = EC_GROUP_new_by_curve_name(nid);
    const char *tmp_q = kgc_q.data();
    const char *tmp_s = kgc_s.data();

    BN_hex2bn(&q, tmp_q);
    BN_hex2bn(&s, tmp_s);
    // BN_rand_range(s, q);
    this->Pub = EC_POINT_new(ec_group);
    EC_POINT_mul(ec_group, Pub, s, nullptr, nullptr, nullptr);
}

std::string KGC::get_s()
{
    return BN_bn2hex(this->s);
}

std::string KGC::get_q()
{
    return BN_bn2hex(this->q);
}

std::string KGC::get_Ppub()
{
    return crypto_utils::point2hex(this->ec_group, this->Pub);
}

KGC::~KGC()
{
    BN_free(this->s);
    BN_free(this->q);
    EC_POINT_free(this->Pub);
    EC_GROUP_free(this->ec_group);
}
