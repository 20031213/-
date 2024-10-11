from configure import *


class ResponseProtocol:
    """服务器响应协议的格式字符串处理"""

    @staticmethod
    def response_login_result(result, nickname, username):
        """
        生成用户登录的结果字符串
        :param result: 0为false，1为ture
        :param nickname: 用户登录昵称，空为失败
        :param username: 用户的账号，空为失败
        :return: 登录的返回响应结果协议信息
        """
        return DELIMITER.join([RESPONSE_LOGIN_RESULT, result, nickname, username])

    @staticmethod
    def response_chat(nickname, message):
        """
        生成用户聊天的结果字符串
        :param nickname: 发送用户登录昵称
        :param message: 用户聊天信息
        :return: 返回聊天响应结果协议信息字符串
        """
        return DELIMITER.join([RESPONSE_CHAT, nickname, message])
