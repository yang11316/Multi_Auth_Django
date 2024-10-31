#ifndef DATA_BUFFER_H
#define DATA_BUFFER_H
#include <queue>
#include <mutex>
#include <condition_variable>
#include <unistd.h>
#include <string>

struct DataInfo
{
    std::string data;
    int len;
    DataInfo()
    {
        len = 0;
    }
};
class DataBuffer
{
private:
    std::queue<DataInfo> data_queue;
    std::mutex m_mutex;
    std::condition_variable m_cond;

public:
    DataBuffer();
    ~DataBuffer();
    void pushData(const std::string data);
    std::string popData();
};
#endif