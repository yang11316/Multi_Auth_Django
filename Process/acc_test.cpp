#include "process_parifree.h"

using namespace std;

mpz_class acc_publickey("a775863f0ad44ca20035dbc8bee624ec9d65415f670e0a7b501bffb6bb298c064d977c6f3a43728ca6a4eca0c35cf0a3957c007de7b601e4302738a734c3bd43a775863f0ad44ca20035dbc8bee624ec9d65415f670e0a7b501bffb6bb298c064d977c6f3a43728ca6a4eca0c35cf0a3957c007de7b601e4302738a734c3bd43", 16);
mpz_class acc_cur("1ab142e1c8f405d4372da735ff0e3ff5b838e05bef312e46002778c6dc3a90ea05aac553711a2a3e5227eba760f530b8fa0aaa53f29208eb2b0caf82a37a53c81ab142e1c8f405d4372da735ff0e3ff5b838e05bef312e46002778c6dc3a90ea05aac553711a2a3e5227eba760f530b8fa0aaa53f29208eb2b0caf82a37a53c8", 16);
bool verify_member(const mpz_class &entity_pid, const mpz_class &entity_witness, const mpz_class &h1)
{
    mpz_class rhs;
    mpz_class acc_hex;
    struct timeval start, end;
    gettimeofday(&start, NULL);
    mpz_powm(rhs.get_mpz_t(), entity_witness.get_mpz_t(), entity_pid.get_mpz_t(),
             acc_publickey.get_mpz_t());
    gettimeofday(&end, NULL);
    long time_use = 1000000 * (end.tv_sec - start.tv_sec) + end.tv_usec - start.tv_usec;
    printf("time use: %ldus\n", time_use);

    mpz_powm(acc_hex.get_mpz_t(), acc_cur.get_mpz_t(), h1.get_mpz_t(),
             acc_publickey.get_mpz_t());
    return acc_hex == rhs;
}

int main()
{
    mpz_class entity_pid("f074b296668195b44f917aed12735ca7", 16);
    mpz_class wit_hex("6ba8fc8c7facd4ef3a2659ee926dc3d24fd08d1b517d8547190295c34879ded7892c9e6ac854053282b81980d9cdf2f9d5ef6019f9db723a384a02e651dadf58ea1b822b6e48ccc041d26db1845ef7cc652cebe808fc551fd94a03069511771bd68f40fc9a5ec2de1761882610101f5370cc14f09df6d5bf0dd2c07b206f5ad1", 16);
    mpz_class h1("b08cc8349f32755f5e13ea95c8ac19f9417b43b79aa574e17e03f3ae43c62e54", 16);
    if (verify_member(entity_pid, wit_hex, h1))
    {
        cout << "Verified" << endl;
    }
    else
    {
        cout << "Not verified" << endl;
    }
}
