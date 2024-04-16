#include <iostream>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <cstring>

int main()
{
    // 创建socket
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1)
    {
        perror("socket creation failed");
        return 1;
    }

    // 服务器地址和端口
    sockaddr_in server_address;
    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(9999);
    if (inet_pton(AF_INET, "192.168.3.17", &server_address.sin_addr) <= 0)
    {
        perror("Invalid address/ Address not supported");
        return 1;
    }

    // 连接到服务器
    if (connect(sock, (struct sockaddr *)&server_address, sizeof(server_address)) < 0)
    {
        perror("connection failed");
        return 1;
    }

    // 发送消息给服务器
    const char *message = "hello";
    send(sock, message, strlen(message), 0);
    std::cout << "Message sent to server: " << message << std::endl;

    // 接收服务器的响应
    char buffer[1024] = {0};
    read(sock, buffer, 1024);
    std::cout << "Response from server: " << buffer << std::endl;

    // 关闭连接
    close(sock);
    return 0;
}
