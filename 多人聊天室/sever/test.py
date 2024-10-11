import socket


def test():
    # 测试基本的服务器连接，数据收发
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(
        ('139.9.76.14', 8090)
    )
    while True:
        message = input("请输入消息")
        client_socket.send(message.encode("UTF-8"))
        recv_data = client_socket.recv(512)
        print(recv_data.decode('UTF-8'))

    client_socket.close()


if __name__ == '__main__':
    test()
