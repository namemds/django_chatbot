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
    conn = pymysql.connect(host="",  # 数据库地址
                           port=0,  # 数据库端口
                           user="",  # 用户名
                           password="",  # 密码
                           database="",  # 数据库名称
                           charset="utf8mb4",
                           cursorclass=pymysql.cursors.DictCursor)
    return conn
