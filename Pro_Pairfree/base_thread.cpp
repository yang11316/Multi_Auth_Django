#include "base_thread.h"

BaseThread::BaseThread()
{
    m_stopflag.store(false);
}

BaseThread::~BaseThread()
{

    if (!m_stopflag.load())
    {
        this->stop();
    }
    if (this->joinable())
    {
        this->m_thread.join();
    }
}

void BaseThread::start()
{
    std::thread t(&BaseThread::run, this);
    this->m_thread = std::move(t);
}

void BaseThread::stop()
{
    // bug fix：子线程生命周期
    // 通知线程停止
    m_stopflag.store(true);
    // 等待线程退出
    if (this->m_thread.joinable())
    {
        this->m_thread.join();
    }
}

void BaseThread::join()
{
    if (!this->m_stopflag.load() && this->m_thread.joinable())
    {
        this->m_thread.join();
    }
}

void BaseThread::detach()
{
    if (!this->m_stopflag.load() && this->m_thread.joinable())
    {
        this->m_thread.join();
    }
}

bool BaseThread::joinable()
{
    return this->m_thread.joinable();
}

bool BaseThread::should_stop() const
{
    return this->m_stopflag.load();
}
