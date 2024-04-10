#include <random>
#include <gmpxx.h>
#include <string>
#include <iostream>

mpz_class test(mpz_class a, mpz_class b, mpz_class c)
{
    mpz_class tmp;
    mpz_mul(tmp.get_mpz_t(), a.get_mpz_t(), b.get_mpz_t());
    mpz_mul(b.get_mpz_t(), a.get_mpz_t(), c.get_mpz_t());
    return tmp;
}

int main()
{
    mpz_class a = 10;
    mpz_class b = 20;
    mpz_class c = 30;
    std::cout << b << std::endl;
    std::cout << test(a, b, c) << std::endl;
}
