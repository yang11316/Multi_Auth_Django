/*
 *@Description: 工具类型函数头文件，包含格式转换，时间间隔等
 */

#pragma once
#include <gmpxx.h>
#include <string>
#include <chrono>
#include <vector>

using chrono_time = std::chrono::_V2::steady_clock::time_point;

namespace utils
{
    // 计算时间间隔
    double count_time(chrono_time start, chrono_time end);

    // string转换成bytes
    std::vector<uint8_t> StringToBytes(const std::string &str);

    // bytes转换成string
    std::string BytesToString(const std::vector<uint8_t> &bytes);

    // 按照bytes进行异或
    std::vector<uint8_t> xorBytes(const std::vector<uint8_t> &data1, const std::vector<uint8_t> &data2);

}