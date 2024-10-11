from configure import *


class RequestProtocol(object):
    @staticmethod
    def request_login_result(username, password):
        """
                生成用户请求登录的字符串
                :param password: 用户密码
                :param username: 用户的账号
                :return: 登录的返回响应结果协议信息
                """
        return DELIMITER.join([REQUEST_LOGIN, username, password])

    @staticmethod
    def request_chat_result(username, message):
        """
        生成用户聊天的结果字符串
        :param username: 发送用户登录账号
        :param message: 用户聊天信息
        :return: 返回聊天响应结果协议信息字符串
        """
        return DELIMITER.join([REQUEST_CHAT, username, message])
