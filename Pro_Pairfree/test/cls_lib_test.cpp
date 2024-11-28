#include <gtest/gtest.h>
#include "config.cpp"
#include "cls_lib.h"

class ClsLibTest : public testing::Test
{
protected:
    std::string ip, ap_ip, domain_id;
    std::uint16_t listening_port, sending_port, ap_port;

    void SetUp() override
    {
        Config config;
        config.loadFromFile("process_config.json");
        ip = config.ip;
        listening_port = config.listening_port;
        sending_port = config.sending_port;
        ap_ip = config.ap_ip;
        ap_port = config.ap_port;
        domain_id = config.domain_id;
    }

    void TearDown() override {}
};

TEST_F(ClsLibTest, HandleKeyUpdate)
{
    CLS_LIB cls(ip, listening_port, sending_port, ap_ip, ap_port);
}

/**
 * 目前正常运行需要注释掉原init方法中启动子进程的run方法
 * 否则报错，信息如下
 * pure virtual method called
 * terminate called without an active exception
 * Aborted (core dumped)
 */
TEST_F(ClsLibTest, HandleInit)
{
    CLS_LIB cls(ip, listening_port, sending_port, ap_ip, ap_port);
    ASSERT_TRUE(cls.init());
}

TEST_F(ClsLibTest, HandleSignAndVerify)
{
    CLS_LIB cls(ip, listening_port, sending_port, ap_ip, ap_port);
    cls.init();
    std::string pid = cls.get_process_pid(), msg = "Hello";
    std::cout << "pid: " + pid << std::endl;
    std::string signed_msg = cls.sign(pid, msg);
    std::cout << "signed_msg: " + signed_msg << std::endl;
    ASSERT_TRUE(cls.verify(pid, signed_msg));
}

sign_payload parse_sign_payload(const std::string &signed_msg)
{
    sign_payload payload;
    std::stringstream ss(signed_msg);
    std::string item;

    while (std::getline(ss, item, '&'))
    {
        if (item.empty())
            continue;
        std::size_t equal_pos = item.find('=');
        if (equal_pos != std::string::npos)
        {
            std::string k = item.substr(0, equal_pos), v = item.substr(equal_pos + 1);
            if (k == "pid")
                payload.pid = v;
            else if (k == "msg")
                payload.msg = v;
            else if (k == "sig1")
                payload.sig1 = v;
            else if (k == "sig2")
                payload.sig2 = v;
            else if (k == "time_stamp")
                payload.time_stamp = v;
            else if (k == "WIT")
                payload.WIT = v;
            else if (k == "wit_hex")
                payload.wit_hex = v;
            else if (k == "X")
                payload.X = v;
        }
    }

    return payload;
}

TEST_F(ClsLibTest, HandleSignAndVerifyWithTampering1)
{
    CLS_LIB cls(ip, listening_port, sending_port, ap_ip, ap_port);
    cls.init();
    std::string pid = cls.get_process_pid(), msg = "Hello";
    std::string signed_msg = cls.sign(pid, msg);
    std::cout << "signed_msg: " + signed_msg << std::endl;

    sign_payload payload = parse_sign_payload(signed_msg);
    payload.msg = "Hallo";
    std::string tampered_signed_msg = "pid=" + payload.pid + "&msg=" + payload.msg + "&sig1=" + payload.sig1 + "&sig2=" + payload.sig2 + "&time_stamp=" + payload.time_stamp + "&WIT=" + payload.WIT + "&wit_hex=" + payload.wit_hex + "&X=" + payload.X + "&domain_id=" + domain_id;
    std::cout << "tampered_signed_msg: " + tampered_signed_msg << std::endl;

    ASSERT_FALSE(cls.verify(pid, tampered_signed_msg));
}

TEST_F(ClsLibTest, HandleSignAndVerifyWithTampering2)
{
    CLS_LIB cls(ip, listening_port, sending_port, ap_ip, ap_port);
    cls.init();
    std::string pid = cls.get_process_pid(), msg = "Hello";
    std::string signed_msg = cls.sign(pid, msg);
    std::cout << "signed_msg: " + signed_msg << std::endl;

    sign_payload payload = parse_sign_payload(signed_msg);
    payload.sig1[1]++;
    std::string tampered_signed_msg = "pid=" + payload.pid + "&msg=" + payload.msg + "&sig1=" + payload.sig1 + "&sig2=" + payload.sig2 + "&time_stamp=" + payload.time_stamp + "&WIT=" + payload.WIT + "&wit_hex=" + payload.wit_hex + "&X=" + payload.X + "&domain_id=" + domain_id;
    std::cout << "tampered_signed_msg: " + tampered_signed_msg << std::endl;

    ASSERT_FALSE(cls.verify(pid, tampered_signed_msg));
}

TEST_F(ClsLibTest, HandleSignAndVerifyWithTampering3)
{
    CLS_LIB cls(ip, listening_port, sending_port, ap_ip, ap_port);
    cls.init();
    std::string pid = cls.get_process_pid(), msg = "Hello";
    std::string signed_msg = cls.sign(pid, msg);
    std::cout << "signed_msg: " + signed_msg << std::endl;

    sign_payload payload = parse_sign_payload(signed_msg);
    payload.sig2[2]++;
    std::string tampered_signed_msg = "pid=" + payload.pid + "&msg=" + payload.msg + "&sig1=" + payload.sig1 + "&sig2=" + payload.sig2 + "&time_stamp=" + payload.time_stamp + "&WIT=" + payload.WIT + "&wit_hex=" + payload.wit_hex + "&X=" + payload.X + "&domain_id=" + domain_id;
    std::cout << "tampered_signed_msg: " + tampered_signed_msg << std::endl;

    ASSERT_FALSE(cls.verify(pid, tampered_signed_msg));
}

int main()
{
    testing::InitGoogleTest();
    return RUN_ALL_TESTS();
}