from pymysql import Connection
from configure import *

# 建立和数据库的连接
conn = Connection(
    host=DB_HOST,
    port=DB_PORT,
    password=DB_PASSWORD,
    user=DB_USER,
    database=DB_NAME,
    charset='utf8mb4'
)
print("con.get_sever_info()")
conn.close()
