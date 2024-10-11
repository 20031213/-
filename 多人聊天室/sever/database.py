from pymysql import connect
from configure import *


class Db(object):
    def __init__(self):
        # 建立和数据库的连接
        self.conn = connect(
            host=DB_HOST,
            database=DB_NAME,
            port=DB_PORT,
            password=DB_PASSWORD,
            user=DB_USER,
            charset='utf8'
        )
        # 获取游标
        self.cursor = self.conn.cursor()

    def close(self):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()

    def get_user(self, sql):
        """
        查询用户的信息
        :param sql: 执行的sql语句
        :return: 把查询后的信息整合成一个字典
        """
        # 执行sql语句
        self.cursor.execute(sql)
        # 获取查询结果
        query_result = self.cursor.fetchone()
        # 是否有查询结果
        if not query_result:
            return None
        # 获取字段名称列表
        fileds = [field[0] for field in self.cursor.description]
        # 使用字段和数据合成字典，供返回使用
        return_data = {}
        for field, value in zip(fileds, query_result):
            return_data[field] = value
        return return_data

    def __del__(self):
        # 析构函数，确保关闭游标和连接
        self.close()


if __name__ == '__main__':
    db = Db()
    user = db.get_user("SELECT * FROM test_user_db where user_name='rq'")
    print(user)
    # 不再需要db对象时，__del__方法会自动调用close方法关闭数据库连接
