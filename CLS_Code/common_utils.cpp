#include "common_utils.h"
#include <iostream>
#include <cstring>
#include <cstdio>
#include <ifaddrs.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <unistd.h>
namespace common_utils
{

    double count_time(chrono_time start, chrono_time end)
    {
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

        double ret = double(duration.count()) * std::chrono::microseconds::period::num / std::chrono::milliseconds::period::den;
        return ret;
    }

    std::vector<uint8_t> StringToBytes(const std::string &str)
    {
        const uint8_t *bytes = reinterpret_cast<const uint8_t *>(str.c_str());
        return std::vector<uint8_t>(bytes, bytes + str.size());
    }

    std::string BytesToString(const std::vector<uint8_t> &bytes)
    {
        const char *str = reinterpret_cast<const char *>(bytes.data());
        return std::string(str, bytes.size());
    }

    std::vector<uint8_t> xorBytes(const std::vector<uint8_t> &data1, const std::vector<uint8_t> &data2)
    {
        std::vector<uint8_t> result;
        size_t minsize = std::min(data1.size(), data2.size());
        for (size_t i = 0; i < minsize; i++)
        {
            result.push_back(data1[i] ^ data2[i]);
        }
        return result;
    }

    std::string getMacAddress(const std::string &interfaceName)
    {
        int sockfd;
        struct ifreq ifr;
        char mac[18] = {0};

        // 创建一个 socket
        sockfd = socket(AF_INET, SOCK_DGRAM, 0);
        if (sockfd < 0)
        {
            perror("socket");
            return "";
        }

        // 设置接口名
        strncpy(ifr.ifr_name, interfaceName.c_str(), IFNAMSIZ - 1);

        // 获取硬件地址
        if (ioctl(sockfd, SIOCGIFHWADDR, &ifr) == 0)
        {
            unsigned char *hwaddr = (unsigned char *)ifr.ifr_hwaddr.sa_data;
            snprintf(mac, sizeof(mac), "%02X:%02X:%02X:%02X:%02X:%02X",
                     hwaddr[0], hwaddr[1], hwaddr[2],
                     hwaddr[3], hwaddr[4], hwaddr[5]);
        }
        else
        {
            perror("ioctl");
            close(sockfd);
            return "";
        }

        close(sockfd);
        std::cout << std::string(mac) << std::endl;
        return std::string(mac);
    }
}
