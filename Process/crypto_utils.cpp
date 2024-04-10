#include "crypto_utils.h"
#include "utils.h"

namespace crypto_utils
{
    mpz_class ex_gcd(mpz_class a, mpz_class b, mpz_class &x, mpz_class &y)
    {
        if (b == 0)
        {
            return x = 1, y = 0, a;
        }
        mpz_class ret = ex_gcd(b, a % b, y, x);
        mpz_class temp = x;
        x = y, y = temp - a / b * y;
        return ret;
    }

    mpz_class mode_reverse(mpz_class a, mpz_class mod)
    {
        mpz_class d, x, y;
        d = ex_gcd(a, mod, x, y);
        if (d == 1)
        {
            return (x % mod + mod) % mod;
        }
        else
        {
            return -1;
        }
    }

    mpz_class quick_mul(mpz_class a, mpz_class b, mpz_class mod)
    {
        mpz_class tmp;
        mpz_mul(tmp.get_mpz_t(), a.get_mpz_t(), b.get_mpz_t());
        mpz_mod(tmp.get_mpz_t(), tmp.get_mpz_t(), mod.get_mpz_t());
        return tmp;
    }

    mpz_class quick_pow(mpz_class a, mpz_class b, mpz_class mod)
    {
        mpz_class tmp;
        mpz_powm(tmp.get_mpz_t(), a.get_mpz_t(), b.get_mpz_t(), mod.get_mpz_t());
        return tmp;
    }

    bool is_prime_miller_rabin(mpz_class num)
    {
        if (num == 2)
            return true; // 2为质数保留
        if (num % 2 != 1 || num < 2)
            return false; // 筛掉偶数和小于2的数
        mpz_class s = 0, t = num - 1;
        while (t % 2 != 1)
        { // 当t为偶数时，继续分解, s递增
            s++;
            t /= 2;
        }
        for (int i = 0; i < 10;
             i++)
        { // 二次探测定理, 进行十次探测, 使方程a^(num-1)=1(mod
          // num)成立的解有仅有a=1或者a=num-1
            gmp_randclass randz(gmp_randinit_default);
            mpz_class a = randz.get_z_range(num - 1); // 随机整数a，取(1, num-1)
            mpz_class x;                              // x为二次探测的解
            mpz_powm(x.get_mpz_t(), a.get_mpz_t(), t.get_mpz_t(),
                     num.get_mpz_t()); // a^t % num
            for (int j = 0; j < s; j++)
            { // x^s=a^(num-1)
                mpz_class test = quick_mul(x, x, num);
                if (test == 1 && x != 1 && x != num - 1)
                    return false; // 若平方取模结果为1，但x不是1或者num-1，则num不是质数
                x = test;
            }
            if (x != 1)
                return false; // 费马小定理
        }
        return true;
    }

    mpz_class rand_big_num(int bits)
    {
        std::random_device rd;
        std::mt19937_64 rng(rd());

        mpz_class mpz_bits = bits;
        gmp_randclass randz(gmp_randinit_default);
        randz.seed(rng());
        return randz.get_z_bits(mpz_bits);
    }

    mpz_class rand_prime(int bits)
    {
        mpz_class prime = rand_big_num(bits);
        mpz_nextprime(prime.get_mpz_t(), prime.get_mpz_t());
        return prime;
    }

    mpz_class rand_safe_prime(int bits)
    {
        gmp_randclass rand(gmp_randinit_default);
        rand.seed(time(NULL));

        mpz_class prime;
        while (true)
        {
            prime = rand.get_z_bits(bits);
            mpz_setbit(prime.get_mpz_t(), 0); // Ensure it's odd

            // Miller-Rabin test with 15 iterations
            if (mpz_probab_prime_p(prime.get_mpz_t(), 15))
            {
                mpz_class tmp = (prime - 1) / 2;

                // Check if (prime - 1) / 2 is also prime
                if (mpz_probab_prime_p(tmp.get_mpz_t(), 15))
                {
                    return prime;
                }
            }
        }
    }

    bool is_safe_prime(mpz_class num)
    {
        if (!is_prime_miller_rabin(num))
            return false;
        mpz_class tmp = (num - 1) / 2;
        if (is_prime_miller_rabin(tmp))
            return true;
        return false;
    }
}