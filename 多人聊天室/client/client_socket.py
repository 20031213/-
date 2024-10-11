import socket
from configure import *


class ClientSocket(socket.socket):
    """自定义套接字，负责初始化客户端套接字需要的相关参数"""

    # 设置为TCP类型
    def __init__(self):
        super(ClientSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)

    def connection(self):
        self.connect(
            (SEVER_IP, SEVER_PORT)
        )

    def recv_data(self):
        """接受数据并解码为字符串"""
        try:
            # 尝试接收数据并解码为UTF-8格式的字符串
            data = self.recv(512)

            if data:
                return data.decode("UTF-8")
            else:
                # 如果接收到的数据为空，可能是连接被对方关闭
                return ""
        except socket.error as e:
            # 捕获套接字错误，并打印错误信息
            print(f"Socket error: {e}")
            return ""
        except UnicodeDecodeError:
            # 捕获解码错误
            print("Data received is not a valid UTF-8 string")
            return ""

    def send_data(self, message):
        """发送数据"""
        return self.send(message.encode("UTF-8"))


if __name__ == '__main__':
    client_socket = ClientSocket()
    client_socket.connection()
