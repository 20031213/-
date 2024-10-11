from threading import Thread
from configure import *
from server_socket import ServerSocket
from wrapper_socket import SocketWrapper
from response_protocol import ResponseProtocol
from database import Db


class Server(object):
    """服务器核心类"""

    def __init__(self):
        # 创建服务器套接字
        self.server_socket = ServerSocket()
        # 创建用户登录和请求函数的字典提高扩展性
        self.request_handle_function = {}
        self.register(REQUEST_LOGIN, self.request_login_handle)
        self.register(REQUEST_CHAT, self.request_chat_handle)
        # 保存当前用户信息的字典
        self.user_data = {}

        # 建立数据库对象db
        self.db = Db()

    def register(self, request_id, handle_function):
        """注册登录请求函数，聊天请求的行为函数"""
        self.request_handle_function[request_id] = handle_function

    def startup(self):
        """获取客户端连接，并提供服务"""
        while True:
            # 获取客户端连接
            print("正在获取客户端连接~~")
            soc, addr = self.server_socket.accept()
            print("获取到客户端连接~~")

            # 使用套接字生成包装对象
            client_soc = SocketWrapper(soc)

            # Thread()函数两个常用值，一个是target用调用函数，应该由于初始化套接字元组
            td = Thread(target=self.request_handle, args=(client_soc,))
            td.start()

    def request_handle(self, client_soc):
        """客户端处理请求"""
        while True:
            recv_data = client_soc.recv_data()
            if not recv_data:
                # 没有接收到数据客户端已经关闭
                self.remove_online_user(client_soc)
                client_soc.close()
                break

            # 解析数据
            parse_data = self.parse_request_text(recv_data)
            print("获取到解析后的内容:%s" % parse_data)
            # 分析数据类型，并根据请求类型调用相应的处理函数

            handle_function = self.request_handle_function.get(parse_data['request_id'])
            if handle_function:
                handle_function(parse_data, client_soc)
            """废弃方案，防止屎山堆积"""
            # if parse_data['request_id'] == REQUEST_LOGIN:
            #     self.request_login_handle(parse_data)
            # elif parse_data['request_id'] == REQUEST_CHAT:
            #     self.request_chat_handle(parse_data)

    def remove_online_user(self, client_soc):
        """客户端下线处理"""
        print("有用户下线~")
        for username, info in self.user_data.items():
            if info["user_soc"] == client_soc:
                del self.user_data[username]
                print(str(self.user_data), '套接字被删除')
                break

    @staticmethod
    def parse_request_text(text):
        """
        解析客户端发来的信息
        登录信息：001|username|password
        聊天信息：002|username|message
        :param text: 传入text变成request_list,然后用“|”分割，再进行字典存储
        :return: 返回request_dict:dictionary
        """

        print("解析客户端数据：" + text)
        # 处理数据使用分隔符DELIMITER然后分别按键值对与响应信息存入字典中
        requests_list = text.split(DELIMITER)
        request_dict = {'request_id': requests_list[0]}

        # 确保请求格式正确
        if len(requests_list) < 3:
            print("请求格式错误，内容:", requests_list)
            return request_dict  # 返回一个空的请求字典

        # 客户登录请求
        if request_dict['request_id'] == REQUEST_LOGIN:
            request_dict['username'] = requests_list[1]
            request_dict['password'] = requests_list[2]
        # 客户聊天请求
        elif request_dict['request_id'] == REQUEST_CHAT:
            request_dict['username'] = requests_list[1]
            request_dict['message'] = requests_list[2]

        return request_dict

    def request_login_handle(self, parse_data, client_soc):
        """
        处理登录功能
        :param client_soc: 客户端的套接字，由于转发功能
        :param parse_data: 传入数据字典用来表明parse_data["username"]用户谁登录
        :return:NONE
        """
        # print("收到登录请求正在处理~~~")
        # # 获取用户登录信息
        # username = parse_data["username"]
        # password = parse_data["password"]
        # # 验证登录是否成功
        # result, nickname, username = self.check_login(username, password)
        # # 登录成功保存用户登录信息
        # if result == "1":
        #     self.user_data['username'] = {"user_soc": client_soc, "nickname": nickname}
        #     # 拼接消息给客户端
        #     response_text = ResponseProtocol.response_login_result(result, nickname, username)
        #     # 把消息给客户端
        #     client_soc.send_data(response_text)
        #     print(f"客户端{parse_data["username"]}登陆成功")
        # else:
        #     fail_text = ResponseProtocol.response_login_result(result, '', '')
        #     client_soc.send_data(fail_text + '您输入错误，请检查账号密码')
        #     print("有人尝试登录但是失败了")

        print("收到登录请求正在处理~~~")
        username = parse_data["username"]
        password = parse_data["password"]
        result, nickname, username = self.check_login(username, password)
        if result == "1":
            self.user_data[username] = {"user_soc": client_soc, "nickname": nickname}
            print(f"客户端{username}登陆成功，昵称：{nickname}")
            response_text = ResponseProtocol.response_login_result(result, nickname, username)
            client_soc.send_data(response_text)
        else:
            fail_text = ResponseProtocol.response_login_result(result, '', '')
            client_soc.send_data(fail_text + '您输入错误，请检查账号密码')
            print("有人尝试登录但是失败了")

    # def request_chat_handle(self, parse_data, client_soc):
    #     """
    #     处理聊天功能
    #     :param client_soc:使用字典把两个函数耦合起来，所以两个参数必须相同，即使用不上，不然删除谁都报错
    #     :param parse_data: 传入数据字典用来表明parse_data["username"]用户谁聊天
    #     :return:
    #     """
    #     print(f"{parse_data['username']}说{parse_data["message"]}")
    #     # 获取消息
    #     sender_username = parse_data['username']
    #     message = parse_data['message']
    #     nickname = self.user_data[sender_username]['nickname']
    #     # 拼接发送给其他客户端消息的文本
    #     chat_text = ResponseProtocol.response_chat(nickname, message)
    #     # 转发消息给在线用户
    #     for u_name, info in self.user_data.items():
    #         if u_name == sender_username:
    #             continue
    #         info["user_soc"].send_data(chat_text)
    def request_chat_handle(self, parse_data, client_soc):
        """
        处理聊天功能
        """
        sender_username = parse_data['username']
        message = parse_data['message']
        try:
            sender_info = self.user_data[sender_username]
            nickname = sender_info['nickname']
        except KeyError:
            print(f"未找到用户 {sender_username} 的信息")
            return  # 直接返回，避免崩溃

        chat_text = ResponseProtocol.response_chat(nickname, message)
        for u_name, info in self.user_data.items():
            if u_name == sender_username:
                continue
            info["user_soc"].send_data(chat_text)

    def check_login(self, username, password):
        """
        从数据库中检查数据，是否正确，或数据库记录
        :param username:用户账号
        :param password:用户密码
        :return:
        """
        # 从数据库中查询信息
        sql = "select * from test_user_db where user_name = '%s'" % username
        result = self.db.get_user(sql)
        # 查询用户是否存在，不存在登录失败
        if not result:
            return '0', '', ''
        # 密码是否正确，密码错误，登陆失败
        if result["user_password"] != password:
            return '0', '', username

        # 否则登录成功
        return '1', result["user_nickname"], username


if __name__ == '__main__':
    Server().startup()
