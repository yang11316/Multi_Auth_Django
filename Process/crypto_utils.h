#pragma once
#include <random>
#include <gmpxx.h>
#include <openssl/bn.h>

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

    // 随机生成指定位数的大数
    mpz_class rand_big_num(int bits);

    // 生成指定位数的素数
    mpz_class rand_prime(int bits);

    // 生成安全素数，计算量大
    mpz_class rand_safe_prime(int bits);

    // 检验是否为安全素数
    bool is_safe_prime(mpz_class num);

}