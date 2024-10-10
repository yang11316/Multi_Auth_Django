#include "utils.h"

namespace utils
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

}
