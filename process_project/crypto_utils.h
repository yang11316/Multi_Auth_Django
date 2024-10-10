/*
 *@Description: 密码学原语工具类型函数头文件
 */
#pragma once
#include <random>
#include <gmpxx.h>
#include <openssl/bn.h>
#include <openssl/ec.h>
#include <openssl/evp.h>
#include <openssl/obj_mac.h>
#include <openssl/md5.h>
#include <string>
#include <iomanip>
#include <sstream>
namespace crypto_utils
{

    // 求两个数的最大公约数,扩展欧几里得算法
    mpz_class ex_gcd(mpz_class a, mpz_class b, mpz_class &x, mpz_class &y);

    // 求a关于mod逆元 ,扩展欧几里得算法
    mpz_class mode_reverse(mpz_class a, mpz_class mod);

    // Miller Rabin 素数判定算法
    bool is_prime_miller_rabin(mpz_class num);

    // 快速乘算法
    mpz_class quick_mul(mpz_class a, mpz_class b, mpz_class mod);

    // 快速幂算法
    mpz_class quick_pow(mpz_class a, mpz_class b, mpz_class mod);

    // 快速幂算法，输入为十六进制字符串
    std::string quickPow_fromhex(std::string &a_hex, std::string &b_hex,
                                 const std::string &N_hex);
    // 获得时间戳
    std::string getTimeStamp();

    // 随机生成指定位数的大数
    mpz_class rand_big_num(int bits);

    // 生成指定位数的素数
    mpz_class rand_prime(int bits);

    // 生成安全素数，计算量大
    mpz_class rand_safe_prime(int bits);

    // 检验是否为安全素数
    bool is_safe_prime(mpz_class num);

    // 椭圆曲线上的点变成十六进制字符串
    std::string point2hex(const EC_GROUP *ec_group, const EC_POINT *point);

    // 将BIGNUM 转换成16进制字符串表示，‘\0’为结束符
    std::string bn2hex(const BIGNUM *bn);
    // 将BIGNUM 转换成10进制字符串表示，‘\0’为结束符
    std::string bn2dec(const BIGNUM *bn);

    // 字符串经过sha256后转成BIGNUM
    BIGNUM *string2hash2bn(const std::string &str);
    // 十进制字符串变成BIGNUM
    BIGNUM *dec2bn(const std::string &dec);
    // 十六进制字符串变成BIGNUM
    BIGNUM *hex2bn(const std::string &hex);
    // 十六进制字符串变成椭圆曲线上的点
    EC_POINT *hex2point(const EC_GROUP *ec_group, const std::string &hex);

    // 求md5值
    std::string get_md5(const std::string &str);
}