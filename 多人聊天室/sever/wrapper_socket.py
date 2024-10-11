import socket


class SocketWrapper(object):
    """套接字包装类"""

    def __init__(self, sock):
        self.sock = sock

    def recv_data(self):
        """接受数据并解码为字符串"""
        try:
            # 尝试接收数据并解码为UTF-8格式的字符串
            data = self.sock.recv(512)

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
        """发送数据并解码为字符串"""
        return self.sock.send(message.encode("UTF-8"))

    def close(self):
        """关闭套接字"""
        self.sock.close()
