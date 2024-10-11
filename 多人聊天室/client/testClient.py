import threading

from windows_login import WindowLogin
from request_protocol import RequestProtocol
from client_socket import ClientSocket
from threading import Thread
from configure import *


class Client(object):

    def __init__(self):
        """初始化客户端资源"""
        # 初始化登录窗口
        self.windows = WindowLogin()
        self.windows.on_reset_click(self.clear_inputs)
        self.windows.on_login_click(self.send_login_data)
        # 创建客户端套接字
        self.conn = ClientSocket()

    def startup(self):
        """开启窗口"""
        self.conn.connection()
        threading.Thread(target=self.response_handle).start()
        self.windows.mainloop()

    def clear_inputs(self):
        self.windows.clear()

    def send_login_data(self):
        """发送消息登录到服务器"""
        # 获取到用户输入账号密码
        username, password = self.windows.get_user_info()
        # 生成协议文本
        request_text = RequestProtocol.request_login_result(username, password)
        # 发送协议文本到服务器
        print(request_text)
        self.conn.send_data(request_text)

    def response_handle(self):
        while True:
            text = self.conn.recv_data()
            print(text)
            parse_data = self.parse_response_text(text)
            print(parse_data)

    @staticmethod
    def parse_response_text(text):
        """
        解析服务器发来的信息
        登录信息：101|result|nickname|username
        聊天信息：102|nickname|message
        :param text: 传入text变成response_list,然后用“|”分割，再进行字典存储
        :return: 返回response_dict:dictionary
        """
        response_list = text.split(DELIMITER)
        response_dict = {'response_id': response_list[0]}
        if response_dict['response_id'] == RESPONSE_LOGIN_RESULT:
            response_dict['result'] = response_list[1]
            response_dict['nickname'] = response_list[2]
            response_dict['username'] = response_list[3]
        elif response_dict['response_id'] == RESPONSE_CHAT:
            response_dict['nickname'] = response_list[1]
            response_dict['message'] = response_list[2]

            return response_dict


if __name__ == '__main__':
    client = Client()
    client.startup()
