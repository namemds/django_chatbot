"""
 配置关于数据库连接信息的文件
 定义一个方法，返回数据库的连接对象
"""
import pymysql


def get_conn():
    """
    获取数据库连接对象
    :return:
    """
    conn = pymysql.connect(host="127.0.0.1",  # 数据库地址
                           port=3306,  # 数据库端口
                           user="root",  # 用户名
                           password="1472138451zh",  # 密码
                           database="uk_ds_users",  # 数据库名称
                           charset="utf8mb4",
                           cursorclass=pymysql.cursors.DictCursor)
    return conn
