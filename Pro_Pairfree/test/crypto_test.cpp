#include <gtest/gtest.h>
#include "process_parifree.h"

/**
 * 1. 初始化
 **/
// 定义测试夹具
class InitTest : public testing::Test
{
protected:
    // 需共享的数据
    std::string entity_pid;
    std::string acc_publickey;
    std::string acc_cur;
    std::string kgc_P;
    std::string entity_witness;
    int nid;

    // 初始化函数
    void SetUp() override
    {
        entity_pid = "cc1b71a101a2091422315e52db4b61c5";
        acc_publickey = "a775863f0ad44ca20035dbc8bee624ec9d65415f670e0a7b501bffb6bb298c064d977c6f3a43728ca6a4eca0c35cf0a3957c007de7b601e4302738a734c3bd43";
        acc_cur = "39859795dc8efa3f73359ef8b259e7e39b48061a8abc00262ac8671187e7a7a7066d7813432534865f96d808087842ce12e5eb933dc52d286f581f6855d7d11b";
        kgc_P = "3db34e39a4c85d2d6e17dd25e8a08c42d349e791b509f6fcfe3e3daaf567a5ca603db34e39a4c85d2d6e17dd25e8a08c42d349e791b509f6fcfe3e3daaf567a5ca6";
        entity_witness = "209d974e66697397ea78cbaa9a81da805e837da10f993010f93f57b8f8098781b149015ff87dfb29b2a06b12612bc5c2a1825dc99805dccdaec0b8f5923b6a18";
        nid = NID_secp256k1;
    }

    // 清理函数
    void TearDown() override {}
};

TEST_F(InitTest, FixtureTest)
{
    ASSERT_TRUE(!entity_pid.empty());
    ASSERT_TRUE(!acc_publickey.empty());
    ASSERT_TRUE(!acc_cur.empty());
    ASSERT_TRUE(!kgc_P.empty());
    ASSERT_TRUE(!entity_witness.empty());
    ASSERT_TRUE(nid);
}

TEST_F(InitTest, FixtureTest2)
{
    EXPECT_EQ(entity_pid, "cc1b71a101a2091422315e52db4b61c5");
    EXPECT_EQ(acc_publickey, "a775863f0ad44ca20035dbc8bee624ec9d65415f670e0a7b501bffb6bb298c064d977c6f3a43728ca6a4eca0c35cf0a3957c007de7b601e4302738a734c3bd43");
    EXPECT_EQ(acc_cur, "39859795dc8efa3f73359ef8b259e7e39b48061a8abc00262ac8671187e7a7a7066d7813432534865f96d808087842ce12e5eb933dc52d286f581f6855d7d11b");
    EXPECT_EQ(kgc_P, "3db34e39a4c85d2d6e17dd25e8a08c42d349e791b509f6fcfe3e3daaf567a5ca603db34e39a4c85d2d6e17dd25e8a08c42d349e791b509f6fcfe3e3daaf567a5ca6");
    EXPECT_EQ(entity_witness, "209d974e66697397ea78cbaa9a81da805e837da10f993010f93f57b8f8098781b149015ff87dfb29b2a06b12612bc5c2a1825dc99805dccdaec0b8f5923b6a18");
    EXPECT_EQ(nid, NID_secp256k1);
}

TEST_F(InitTest, HandleInputThroughEmptyConstructor)
{
    Process *p = new Process();
    ASSERT_NE(p, nullptr);
}

TEST_F(InitTest, HandleValidInputThroughConstructor)
{
    Process *p = new Process(entity_pid, acc_publickey, acc_cur, entity_witness, kgc_P);

    EXPECT_EQ(p->pid, entity_pid);
    EXPECT_EQ(p->acc_witness, mpz_class(entity_witness, 16));
    EXPECT_EQ(p->acc_cur, mpz_class(acc_cur, 16));
    EXPECT_EQ(p->acc_publickey, mpz_class(acc_publickey, 16));

    ASSERT_NE(p->ec_group, nullptr);
    EXPECT_TRUE(!EC_GROUP_cmp(p->ec_group, EC_GROUP_new_by_curve_name(nid), nullptr));
    EXPECT_TRUE(!BN_cmp(p->q, EC_GROUP_get0_order(p->ec_group)));
    EXPECT_TRUE(!EC_POINT_cmp(p->ec_group, p->Pub, crypto_utils::hex2point(p->ec_group, kgc_P), nullptr));

    EXPECT_TRUE(p->is_init);
}

TEST_F(InitTest, HandleFullInputThroughConstructor)
{
    Process *p = new Process(entity_pid, acc_publickey, acc_cur, entity_witness, kgc_P, nid);

    EXPECT_EQ(p->pid, entity_pid);
    EXPECT_EQ(p->acc_witness, mpz_class(entity_witness, 16));
    EXPECT_EQ(p->acc_cur, mpz_class(acc_cur, 16));
    EXPECT_EQ(p->acc_publickey, mpz_class(acc_publickey, 16));

    ASSERT_NE(p->ec_group, nullptr);
    EXPECT_TRUE(!EC_GROUP_cmp(p->ec_group, EC_GROUP_new_by_curve_name(nid), nullptr));
    EXPECT_TRUE(!BN_cmp(p->q, EC_GROUP_get0_order(p->ec_group)));
    EXPECT_TRUE(!EC_POINT_cmp(p->ec_group, p->Pub, crypto_utils::hex2point(p->ec_group, kgc_P), nullptr));

    EXPECT_TRUE(p->is_init);
}

TEST_F(InitTest, HandlePartialInputThroughConstructor)
{
    // Process *p = new Process(entity_pid, acc_publickey, acc_cur, kgc_P);
    Process *p = new Process(acc_publickey, acc_cur, kgc_P);

    EXPECT_EQ(p->pid, entity_pid);
    EXPECT_EQ(p->acc_cur, mpz_class(acc_cur, 16));
    EXPECT_EQ(p->acc_publickey, mpz_class(acc_publickey, 16));

    ASSERT_NE(p->ec_group, nullptr);
    EXPECT_TRUE(!EC_GROUP_cmp(p->ec_group, EC_GROUP_new_by_curve_name(nid), nullptr));
    EXPECT_TRUE(!BN_cmp(p->q, EC_GROUP_get0_order(p->ec_group)));
    EXPECT_TRUE(!EC_POINT_cmp(p->ec_group, p->Pub, crypto_utils::hex2point(p->ec_group, kgc_P), nullptr));

    EXPECT_TRUE(p->is_init);
}

TEST_F(InitTest, HandleValidInput)
{
    Process *p = new Process();

    p->init(entity_pid, acc_publickey, acc_cur, entity_witness, kgc_P);

    EXPECT_EQ(p->pid, entity_pid);
    EXPECT_EQ(p->acc_cur, mpz_class(acc_cur, 16));
    EXPECT_EQ(p->acc_publickey, mpz_class(acc_publickey, 16));

    ASSERT_NE(p->ec_group, nullptr);
    EXPECT_TRUE(!EC_GROUP_cmp(p->ec_group, EC_GROUP_new_by_curve_name(nid), nullptr));
    EXPECT_TRUE(!BN_cmp(p->q, EC_GROUP_get0_order(p->ec_group)));
    EXPECT_TRUE(!EC_POINT_cmp(p->ec_group, p->Pub, crypto_utils::hex2point(p->ec_group, kgc_P), nullptr));

    EXPECT_TRUE(p->is_init);
}

TEST_F(InitTest, HandleFullInput)
{
    Process *p = new Process();

    p->init(entity_pid, acc_publickey, acc_cur, entity_witness, kgc_P, nid);

    EXPECT_EQ(p->pid, entity_pid);
    EXPECT_EQ(p->acc_witness, mpz_class(entity_witness, 16));
    EXPECT_EQ(p->acc_cur, mpz_class(acc_cur, 16));
    EXPECT_EQ(p->acc_publickey, mpz_class(acc_publickey, 16));

    ASSERT_NE(p->ec_group, nullptr);
    EXPECT_TRUE(!EC_GROUP_cmp(p->ec_group, EC_GROUP_new_by_curve_name(nid), nullptr));
    EXPECT_TRUE(!BN_cmp(p->q, EC_GROUP_get0_order(p->ec_group)));
    EXPECT_TRUE(!EC_POINT_cmp(p->ec_group, p->Pub, crypto_utils::hex2point(p->ec_group, kgc_P), nullptr));

    EXPECT_TRUE(p->is_init);
}

/**
 * 计算初始化耗时
*/
TEST_F(InitTest, HandleTimeUse)
{
    Process *p = new Process();

    int tot = 50, i = tot;
    long long t = 0;
    while (i--) {
        struct timeval begtime, endtime;
        gettimeofday(&begtime, NULL);
        p->init(entity_pid, acc_publickey, acc_cur, entity_witness, kgc_P);
        gettimeofday(&endtime, NULL);
        t += 1000000 * (endtime.tv_sec - begtime.tv_sec) + endtime.tv_usec - begtime.tv_usec;
    }

    printf("初始化%d次的平均耗时: %lld us\n", tot, t / tot);
}

TEST_F(InitTest, HandlePartialInput)
{
    Process *p = new Process();
    // 不指定nid
    p->init(entity_pid, acc_publickey, acc_cur, kgc_P);

    EXPECT_EQ(p->pid, entity_pid);
    EXPECT_EQ(p->acc_cur, mpz_class(acc_cur, 16));
    EXPECT_EQ(p->acc_publickey, mpz_class(acc_publickey, 16));

    ASSERT_NE(p->ec_group, nullptr);
    EXPECT_TRUE(!EC_GROUP_cmp(p->ec_group, EC_GROUP_new_by_curve_name(nid), nullptr));
    EXPECT_TRUE(!BN_cmp(p->q, EC_GROUP_get0_order(p->ec_group)));
    EXPECT_TRUE(!EC_POINT_cmp(p->ec_group, p->Pub, crypto_utils::hex2point(p->ec_group, kgc_P), nullptr));

    EXPECT_TRUE(p->is_init);
}

TEST_F(InitTest, HandleInvalidInput)
{
    Process *p = new Process();
    // 证据值置空
    std::string empty_entity_witness = "";
    EXPECT_THROW(p->init(entity_pid, acc_publickey, acc_cur, empty_entity_witness, kgc_P), std::invalid_argument);

    EXPECT_FALSE(p->is_init);
}

/**
 * 2. 生成完整密钥
 **/
class KeyGenerationTest : public testing::Test
{
protected:
    std::string entity_pid;
    std::string acc_publickey;
    std::string acc_cur;
    std::string kgc_P;
    std::string entity_witness;

    void SetUp() override
    {
        entity_pid = "99bab9c0c59f0154f49b1b15c3d62257";
        acc_publickey = "a775863f0ad44ca20035dbc8bee624ec9d65415f670e0a7b501bffb6bb298c064d977c6f3a43728ca6a4eca0c35cf0a3957c007de7b601e4302738a734c3bd43";
        acc_cur = "39859795dc8efa3f73359ef8b259e7e39b48061a8abc00262ac8671187e7a7a7066d7813432534865f96d808087842ce12e5eb933dc52d286f581f6855d7d11b";
        kgc_P = "3db34e39a4c85d2d6e17dd25e8a08c42d349e791b509f6fcfe3e3daaf567a5ca603db34e39a4c85d2d6e17dd25e8a08c42d349e791b509f6fcfe3e3daaf567a5ca6";
        entity_witness = "a6ce2377bfc63b8232add83ec40cda7b49d553a5a28351317fc64e1bacc9aa65233a597ae0ffb2117e43d67e8418bfd651ccf975835b135ae3719b1cd0fef706";
    }

    void TearDown() override {}
};

TEST_F(KeyGenerationTest, FixtureTest)
{
    ASSERT_TRUE(!entity_pid.empty());
    ASSERT_TRUE(!acc_publickey.empty());
    ASSERT_TRUE(!acc_cur.empty());
    ASSERT_TRUE(!kgc_P.empty());
    ASSERT_TRUE(!entity_witness.empty());
}

TEST_F(KeyGenerationTest, FixtureTest2)
{
    EXPECT_EQ(entity_pid, "99bab9c0c59f0154f49b1b15c3d62257");
    EXPECT_EQ(acc_publickey, "a775863f0ad44ca20035dbc8bee624ec9d65415f670e0a7b501bffb6bb298c064d977c6f3a43728ca6a4eca0c35cf0a3957c007de7b601e4302738a734c3bd43");
    EXPECT_EQ(acc_cur, "39859795dc8efa3f73359ef8b259e7e39b48061a8abc00262ac8671187e7a7a7066d7813432534865f96d808087842ce12e5eb933dc52d286f581f6855d7d11b");
    EXPECT_EQ(kgc_P, "3db34e39a4c85d2d6e17dd25e8a08c42d349e791b509f6fcfe3e3daaf567a5ca603db34e39a4c85d2d6e17dd25e8a08c42d349e791b509f6fcfe3e3daaf567a5ca6");
    EXPECT_EQ(entity_witness, "a6ce2377bfc63b8232add83ec40cda7b49d553a5a28351317fc64e1bacc9aa65233a597ae0ffb2117e43d67e8418bfd651ccf975835b135ae3719b1cd0fef706");
}

TEST_F(KeyGenerationTest, HandleFullKeyGeneration)
{
    Process *p = new Process(entity_pid, acc_publickey, acc_cur, entity_witness, kgc_P);

    p->generate_full_key();

    ASSERT_NE(p->X, nullptr);
    ASSERT_NE(p->WIT, nullptr);

    BIGNUM *h1_str = crypto_utils::string2hash2bn(p->pid + crypto_utils::point2hex(p->ec_group, p->WIT) + crypto_utils::point2hex(p->ec_group, p->X));
    mpz_class mpz_h1 = mpz_class(crypto_utils::bn2hex(h1_str), 16);
    mpz_class tmp = crypto_utils::quick_pow(p->acc_witness, mpz_h1, p->acc_publickey);
    BIGNUM *wit_hash = crypto_utils::hex2bn(tmp.get_str(16));
    EXPECT_TRUE(!BN_cmp(p->wit_hash, wit_hash));

    EXPECT_TRUE(p->is_fullkey);
}

/**
 * 计算密钥生成耗时
*/
TEST_F(KeyGenerationTest, HandleTimeUse)
{
    Process *p = new Process();
    p->init(entity_pid, acc_publickey, acc_cur, entity_witness, kgc_P);

    int tot = 50, i = tot;
    long long t = 0;
    while (i--) {
        struct timeval begtime, endtime;
        gettimeofday(&begtime, NULL);
        p->generate_full_key();
        gettimeofday(&endtime, NULL);
        t += 1000000 * (endtime.tv_sec - begtime.tv_sec) + endtime.tv_usec - begtime.tv_usec;
    }

    printf("生成%d次密钥的平均耗时: %lld us\n", tot, t / tot);
}

/**
 * 3. 签名与验证
 **/
class SignAndVerifyTest : public testing::Test
{
protected:
    std::string entity_pid;
    std::string acc_publickey;
    std::string acc_cur;
    std::string kgc_P;
    std::string entity_witness;
    void SetUp() override
    {
        entity_pid = "6164916b3314f2ce4a3150e9173a5179";
        acc_publickey = "a775863f0ad44ca20035dbc8bee624ec9d65415f670e0a7b501bffb6bb298c064d977c6f3a43728ca6a4eca0c35cf0a3957c007de7b601e4302738a734c3bd43";
        acc_cur = "1ab142e1c8f405d4372da735ff0e3ff5b838e05bef312e46002778c6dc3a90ea05aac553711a2a3e5227eba760f530b8fa0aaa53f29208eb2b0caf82a37a53c8";
        kgc_P = "3db34e39a4c85d2d6e17dd25e8a08c42d349e791b509f6fcfe3e3daaf567a5ca603db34e39a4c85d2d6e17dd25e8a08c42d349e791b509f6fcfe3e3daaf567a5ca6";
        entity_witness = "57bcfebcde5b373a6d14916d50585f9f39152ff5bf95ab9f1ba5b7447a02112851b345c3ff6a0bc1fd9c404d3905e9b4eba68bcd6220d32d91929c6606a464c5";
    }

    void TearDown() override {}
};

TEST_F(SignAndVerifyTest, FixtureTest)
{
    ASSERT_TRUE(!entity_pid.empty());
    ASSERT_TRUE(!acc_publickey.empty());
    ASSERT_TRUE(!acc_cur.empty());
    ASSERT_TRUE(!kgc_P.empty());
    ASSERT_TRUE(!entity_witness.empty());
}

TEST_F(SignAndVerifyTest, FixtureTest2)
{
    EXPECT_EQ(entity_pid, "6164916b3314f2ce4a3150e9173a5179");
    EXPECT_EQ(acc_publickey, "a775863f0ad44ca20035dbc8bee624ec9d65415f670e0a7b501bffb6bb298c064d977c6f3a43728ca6a4eca0c35cf0a3957c007de7b601e4302738a734c3bd43");
    EXPECT_EQ(acc_cur, "1ab142e1c8f405d4372da735ff0e3ff5b838e05bef312e46002778c6dc3a90ea05aac553711a2a3e5227eba760f530b8fa0aaa53f29208eb2b0caf82a37a53c8");
    EXPECT_EQ(kgc_P, "3db34e39a4c85d2d6e17dd25e8a08c42d349e791b509f6fcfe3e3daaf567a5ca603db34e39a4c85d2d6e17dd25e8a08c42d349e791b509f6fcfe3e3daaf567a5ca6");
    EXPECT_EQ(entity_witness, "57bcfebcde5b373a6d14916d50585f9f39152ff5bf95ab9f1ba5b7447a02112851b345c3ff6a0bc1fd9c404d3905e9b4eba68bcd6220d32d91929c6606a464c5");
}

TEST_F(SignAndVerifyTest, HandleValidInput)
{
    Process *p = new Process(entity_pid, acc_publickey, acc_cur, entity_witness, kgc_P);

    struct timeval begtime, endtime;
    gettimeofday(&begtime, NULL);
    p->generate_full_key();
    gettimeofday(&endtime, NULL);
    long timeuse = 1000000 * (endtime.tv_sec - begtime.tv_sec) + endtime.tv_usec - begtime.tv_usec;
    printf("密钥生成耗时: %ld us\n", timeuse);

    std::string msg = "hello";

    struct timeval signBeginTime, signEndTime;
    gettimeofday(&signBeginTime, NULL);
    sign_payload payload = p->sign(msg);
    gettimeofday(&signEndTime, NULL);
    long signTimeUse = 1000000 * (signEndTime.tv_sec - signBeginTime.tv_sec) + signEndTime.tv_usec - signBeginTime.tv_usec;
    printf("签名耗时: %ld us\n", signTimeUse);

    struct timeval verifyBeginTime, verifyEndTime;
    gettimeofday(&verifyBeginTime, NULL);
    bool res = p->verify_sign(payload);
    gettimeofday(&verifyEndTime, NULL);
    long verifyTimeUse = 1000000 * (verifyEndTime.tv_sec - verifyBeginTime.tv_sec) + verifyEndTime.tv_usec - verifyBeginTime.tv_usec;
    printf("验签耗时: %ld us\n", verifyTimeUse);

    EXPECT_TRUE(res);
}

/**
 * 计算签名和验签耗时
*/
TEST_F(SignAndVerifyTest, HandleTimeUse)
{
    Process *p = new Process(entity_pid, acc_publickey, acc_cur, entity_witness, kgc_P);

    p->generate_full_key();

    int tot = 50, i = tot;
    std::string msg = "hello";
    long long t1 = 0, t2 = 0;
    while (i--) {
        struct timeval signBeginTime, signEndTime;
        gettimeofday(&signBeginTime, NULL);
        sign_payload payload = p->sign(msg);
        gettimeofday(&signEndTime, NULL);
        t1 += 1000000LL * (signEndTime.tv_sec - signBeginTime.tv_sec) + (signEndTime.tv_usec - signBeginTime.tv_usec);

        struct timeval verifyBeginTime, verifyEndTime;
        gettimeofday(&verifyBeginTime, NULL);
        bool res = p->verify_sign(payload);
        gettimeofday(&verifyEndTime, NULL);
        t2 += 1000000LL * (verifyEndTime.tv_sec - verifyBeginTime.tv_sec) + (verifyEndTime.tv_usec - verifyBeginTime.tv_usec);

        EXPECT_TRUE(res);
    }

    printf("签名%d次的平均耗时: %lld us\n", tot, t1 / tot);
    printf("验证%d次的平均耗时: %lld us\n", tot, t2 / tot);
}

TEST_F(SignAndVerifyTest, HandleMsgTampering)
{
    Process *p = new Process(entity_pid, acc_publickey, acc_cur, entity_witness, kgc_P);
    p->generate_full_key();
    std::string msg = "hello";
    sign_payload payload = p->sign(msg);

    payload.msg[0]++;

    EXPECT_FALSE(p->verify_sign(payload));
}

TEST_F(SignAndVerifyTest, HandleSig1Tampering)
{
    Process *p = new Process(entity_pid, acc_publickey, acc_cur, entity_witness, kgc_P);
    p->generate_full_key();
    std::string msg = "hello";
    sign_payload payload = p->sign(msg);

    payload.sig1[1]++;

    EXPECT_FALSE(p->verify_sign(payload));
}

TEST_F(SignAndVerifyTest, HandleSig2Tampering)
{
    Process *p = new Process(entity_pid, acc_publickey, acc_cur, entity_witness, kgc_P);
    p->generate_full_key();
    std::string msg = "hello";
    sign_payload payload = p->sign(msg);

    payload.sig2[2]++;

    EXPECT_FALSE(p->verify_sign(payload));
}

/**
 * 4. 密钥更新
 **/
TEST(KeyUpdateTest, HandleValidTest)
{
    std::string entity_pid = "6164916b3314f2ce4a3150e9173a5179";
    std::string acc_publickey = "a775863f0ad44ca20035dbc8bee624ec9d65415f670e0a7b501bffb6bb298c064d977c6f3a43728ca6a4eca0c35cf0a3957c007de7b601e4302738a734c3bd43";
    std::string acc_cur = "1ab142e1c8f405d4372da735ff0e3ff5b838e05bef312e46002778c6dc3a90ea05aac553711a2a3e5227eba760f530b8fa0aaa53f29208eb2b0caf82a37a53c8";
    std::string kgc_P = "3db34e39a4c85d2d6e17dd25e8a08c42d349e791b509f6fcfe3e3daaf567a5ca603db34e39a4c85d2d6e17dd25e8a08c42d349e791b509f6fcfe3e3daaf567a5ca6";
    std::string entity_witness = "57bcfebcde5b373a6d14916d50585f9f39152ff5bf95ab9f1ba5b7447a02112851b345c3ff6a0bc1fd9c404d3905e9b4eba68bcd6220d32d91929c6606a464c5";

    Process *p = new Process(entity_pid, acc_publickey, acc_cur, entity_witness, kgc_P);

    // 首次生成密钥
    p->generate_full_key();
    ASSERT_NE(p->X, nullptr);
    ASSERT_NE(p->WIT, nullptr);
    BIGNUM *h1_str = crypto_utils::string2hash2bn(p->pid + crypto_utils::point2hex(p->ec_group, p->WIT) + crypto_utils::point2hex(p->ec_group, p->X));
    mpz_class mpz_h1 = mpz_class(crypto_utils::bn2hex(h1_str), 16);
    mpz_class tmp = crypto_utils::quick_pow(p->acc_witness, mpz_h1, p->acc_publickey);
    BIGNUM *wit_hash = crypto_utils::hex2bn(tmp.get_str(16));
    EXPECT_TRUE(!BN_cmp(p->wit_hash, wit_hash));
    EXPECT_TRUE(p->is_fullkey);

    // 更新密钥
    std::string new_entity_pid = "64a57cc12951bd9a84b4a2ba12d51c79";

    struct timeval begtime, endtime;
    gettimeofday(&begtime, NULL);
    p->update_key(new_entity_pid);
    gettimeofday(&endtime, NULL);
    long timeuse = 1000000 * (endtime.tv_sec - begtime.tv_sec) + endtime.tv_usec - begtime.tv_usec;
    printf("key update time: %ld us\n", timeuse);

    EXPECT_NE(p->acc_witness, mpz_class(entity_witness, 16));
    EXPECT_NE(p->acc_cur, mpz_class(acc_cur, 16));
    ASSERT_NE(p->X, nullptr);
    ASSERT_NE(p->WIT, nullptr);
    BIGNUM *h1_str_new = crypto_utils::string2hash2bn(p->pid + crypto_utils::point2hex(p->ec_group, p->WIT) + crypto_utils::point2hex(p->ec_group, p->X));
    mpz_class mpz_h1_new = mpz_class(crypto_utils::bn2hex(h1_str_new), 16);
    mpz_class tmp_new = crypto_utils::quick_pow(p->acc_witness, mpz_h1_new, p->acc_publickey);
    BIGNUM *wit_hash_new = crypto_utils::hex2bn(tmp_new.get_str(16));
    EXPECT_FALSE(!BN_cmp(p->wit_hash, wit_hash));
    EXPECT_TRUE(!BN_cmp(p->wit_hash, wit_hash_new));

    // std::string msg = "hello";
    // sign_payload payload = p->sign(msg);

    // EXPECT_TRUE(p->verify_sign(payload));
}

// 测试

int main()
{
    testing::InitGoogleTest();
    return RUN_ALL_TESTS();
}