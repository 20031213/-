import sys
from threading import Thread
from tkinter.messagebox import showinfo

from client_socket import ClientSocket
from configure import *
from request_protocol import RequestProtocol
from windows_chat import WindowsChat
from windows_login import WindowLogin


class Client(object):

    def __init__(self):
        """初始化客户端资源"""
        # 初始化登录窗口
        self.windows = WindowLogin()
        self.windows.on_reset_click(self.clear_inputs)
        self.windows.on_login_click(self.send_login_data)
        self.response_handle_function = {}
        self.register(RESPONSE_LOGIN_RESULT, self.response_login_handle)
        self.register(RESPONSE_CHAT, self.response_chat_handle)
        self.windows.on_window_close(self.exit)

        # 创建聊天窗口
        self.windows_chat = WindowsChat()
        self.windows_chat.withdraw()  # 隐藏窗口
        self.windows_chat.on_send_button(self.send_chat_data)
        self.windows_chat.on_window_closed(self.exit)
        # 创建客户端套接字
        self.conn = ClientSocket()

        # 在线用户名
        self.username = None

        # 程序运行的标记
        self.running_flag = True

    def register(self, request_id, handle_function):
        """注册登录请求函数，聊天请求的行为函数"""
        self.response_handle_function[request_id] = handle_function

    def startup(self):
        """开启窗口"""
        self.conn.connection()
        Thread(target=self.response_handle).start()
        self.windows.mainloop()

    def clear_inputs(self):
        self.windows.clear()

    def send_login_data(self):
        """发送消息登录到服务器"""
        # 获取到用户输入账号密码
        self.username, password = self.windows.get_user_info()
        # 生成协议文本
        request_text = RequestProtocol.request_login_result(self.username, password)
        # 发送协议文本到服务器
        print(request_text)
        self.conn.send_data(request_text)

    def response_handle(self):
        while self.running_flag:
            text = self.conn.recv_data()
            print(text)
            parse_data = self.parse_response_text(text)
            handle_function = self.response_handle_function.get(parse_data['response_id'])
            if handle_function:
                handle_function(parse_data)

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

    def response_login_handle(self, parse_data):
        """登录响应"""
        result = parse_data['result']
        if result == '0':
            """
            showinfo有两个参数title是标题，message是内容
            """
            showinfo("tips", "您登陆失败，请检查密码和账号是否正确")
            print('您登陆失败，请检查密码和账号是否正确')
            return

        showinfo("tips", "登陆成功，欢迎使用rq聊天SF")
        # 登陆成功获取用户消息
        nickname = parse_data['nickname']
        self.username = parse_data['username']
        # 登陆成功显示聊天窗口与标题，隐藏登录窗口
        self.windows_chat.welcome(nickname)
        self.windows_chat.update()
        self.windows_chat.deiconify()

        self.windows.withdraw()

    def response_chat_handle(self, response_dict):
        """聊天消息响应"""
        sender = response_dict['nickname']
        message = response_dict['message']
        self.windows_chat.append_text(sender, message)

    def send_chat_data(self):
        """获取输入内容，发送到服务器"""
        # 获取输入
        message = self.windows_chat.get_input_text()
        self.windows_chat.clear_input()  # 清空输入框

        # 拼接协议文本
        chat_text = RequestProtocol.request_chat_result(self.username, message)

        # 发送消息内容
        self.conn.send_data(chat_text)

        # 立即在聊天窗口中显示发送的消息
        self.windows_chat.append_text('我', message)

    def exit(self):
        self.running_flag = False  # 停止子线程
        self.conn.close()   # 关闭套接字
        sys.exit()  # 停止线程


if __name__ == '__main__':
    client = Client()
    client.startup()
