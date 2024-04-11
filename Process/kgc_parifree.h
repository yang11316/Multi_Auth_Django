/*
 *@Description: 密钥生成中心
 */
#ifndef KGC_H
#define KGC_H
#pragma once
#include "crypto_utils.h"

class KGC
{
private:
    BIGNUM *s = NULL;

public:
    EC_GROUP *ec_group;
    BIGNUM *q = NULL;
    EC_POINT *Pub;

    explicit KGC(int nid = NID_secp256k1);

    explicit KGC(const std::string &s, const std::string &q, int nid = NID_secp256k1);
    std::string get_s();
    std::string get_q();
    std::string get_Ppub();

    ~KGC();
};

#endif