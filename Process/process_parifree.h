/*
 *@Description: 进程类
 */

#pragma once
#include "crypto_utils.h"
#include <iostream>
struct sign_payload
{
    std::string pid;
    std::string msg;
    std::string X, WIT, wit_hex;
    std::string sig1, sig2;
    std::string time_stamp;
};

class Process
{

public:
    // 累加器相关参数
    mpz_class acc_cur;
    mpz_class acc_publickey;
    mpz_class acc_witness;
    // 无证书签名参数
    std::string pid;
    EC_GROUP *ec_group;
    BIGNUM *q;
    // kgc的公钥
    EC_POINT *Pub;
    std::tuple<EC_POINT *, EC_POINT *, BIGNUM *> public_key;

    // 初始化，输入pid、acc公钥、acc目前值、自己证据值、椭圆曲线P、acc当前值所在椭圆曲线组
    Process(const std::string &entity_pid, const std::string &acc_publickey, const std::string &acc_cur, const std::string &entity_witness, const std::string &kgc_P, int nid = NID_secp256k1);

    // 密码学累加器验证
    bool verify_member(const mpz_class &entity_pid, const mpz_class &entity_witness, const mpz_class &h1);
    // 累加器值更新
    void update_witness(const mpz_class &aux);

    // 生成完整密钥
    bool generate_full_key();

    // 签名
    sign_payload sign(const std::string &msg);

    // 验证签名
    bool verify_sign(const sign_payload &payload);

private:
    std::pair<BIGNUM *, BIGNUM *> secret_key;
};
