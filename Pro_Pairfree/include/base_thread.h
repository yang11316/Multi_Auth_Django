#include <thread>
#include <atomic>

class BaseThread
{
public:
    BaseThread();
    virtual ~BaseThread();

    void start();
    void stop();
    void join();
    void detach();
    bool joinable();

protected:
    bool should_stop() const;
    virtual void run() = 0;

private:
    std::atomic<bool> m_stopflag;
    std::thread m_thread;
};
