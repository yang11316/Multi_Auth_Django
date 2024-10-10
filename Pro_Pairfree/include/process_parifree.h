/*
 *@Description: 进程类
 */
#ifndef _PROCESS_PARIFREE_H
#define _PROCESS_PARIFREE_H
#pragma once

#include "crypto_utils.h"
#include <iostream>
#include <sys/time.h>
struct sign_payload
{
    std::string pid;
    std::string msg;
    std::string X, WIT, wit_hex;
    std::string sig1, sig2;
    std::string time_stamp;

    std::string to_string()
    {
        std::stringstream ss;
        ss << "pid=" << pid << "&msg=" << msg << "&X=" << X << "&WIT=" << WIT << "&wit_hex=" << wit_hex << "&sig1=" << sig1 << "&sig2=" << sig2 << "&time_stamp=" << time_stamp;
        return ss.str();
    }
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

    // 自己公钥
    EC_POINT *X;
    EC_POINT *WIT;
    BIGNUM *wit_hash;
    // 判断是否初始化
    bool is_init = false;
    // 判断是否生成完整公私钥
    bool is_fullkey = false;

    // 初始化，输入pid、acc公钥、acc目前值、自己证据值、椭圆曲线P、acc当前值所在椭圆曲线组
    Process();
    Process(const std::string &entity_pid, const std::string &acc_publickey, const std::string &acc_cur, const std::string &kgc_P, int nid = NID_secp256k1);
    Process(const std::string &entity_pid, const std::string &acc_publickey, const std::string &acc_cur, const std::string &entity_witness, const std::string &kgc_P, int nid = NID_secp256k1);

    void init(const std::string &entity_pid, const std::string &acc_publickey, const std::string &acc_cur, const std::string &entity_witness, const std::string &kgc_P, int nid = NID_secp256k1);
    void init(const std::string &entity_pid, const std::string &acc_publickey, const std::string &acc_cur, const std::string &kgc_P, int nid = NID_secp256k1);

    // 生成完整密钥
    bool generate_full_key();

    // 签名
    sign_payload sign(const std::string &msg);

    // 验证签名
    bool verify_sign(const sign_payload &payload);

    // 公私钥更新
    void update_key(const std::string &aux);

private:
    // 私钥
    BIGNUM *x;
    BIGNUM *wit;
    // 密码学累加器验证
    bool verify_member(const mpz_class &entity_pid, const mpz_class &entity_witness, const mpz_class &h1);
    // 证据值更新
    void update_witness(const mpz_class &aux);
    // 累加值更新
    void update_accumulator(const mpz_class &aux);
};

#endif