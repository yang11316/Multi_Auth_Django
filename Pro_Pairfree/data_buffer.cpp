#include "data_buffer.h"

DataBuffer::DataBuffer()
{
}

DataBuffer::~DataBuffer()
{
}

void DataBuffer::pushData(const std::string data)
{
    DataInfo info;
    info.data = data.c_str();
    info.len = data.length();
    std::lock_guard<std::mutex> lock(m_mutex);
    data_queue.push(info);
    m_cond.notify_one();
}

std::string DataBuffer::popData()
{
    std::unique_lock<std::mutex> lock(m_mutex);
    while (data_queue.empty())
    {
        m_cond.wait(lock);
    }
    DataInfo info = data_queue.front();
    data_queue.pop();
    return std::string(info.data, info.len);
}
