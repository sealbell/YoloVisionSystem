import pymysql


class OperationMysql:
    # 创建一个连接数据库的对象
    def __init__(self):
        self.conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,  # 数据库端口号(一般为：3306)
            user="root",  # 数据库登录用户名
            passwd="123456",  # 数据库登录密码
            db="yolov5",  # 数据库名称
            charset='utf8',  # 连接编码
            cursorclass=pymysql.cursors.DictCursor
        )

    # 查询数据
    def search(self, sql):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(sql)
                result = cur.fetchall()
                return result

    # 更新SQL
    def update_one(self, sql):
        with self.conn:
            with self.conn.cursor() as cur:
                try:
                    cur.execute(sql)  # 执行sql
                    self.conn.commit()  # 增删改操作完数据库后，需要执行提交操作
                except:
                    # 发生错误时回滚
                    self.conn.rollback()

    # 插入SQL
    def insert_one(self, sql):
        with self.conn:
            with self.conn.cursor() as cur:
                try:
                    cur.execute(sql)  # 执行sql
                    self.conn.commit()  # 增删改操作完数据库后，需要执行提交操作
                except:
                    # 发生错误时回滚
                    self.conn.rollback()

    # 删除sql
    def delete_one(self, sql):
        with self.conn:
            with self.conn.cursor() as cur:
                try:
                    cur.execute(sql)  # 执行sql
                    self.conn.commit()  # 增删改操作完数据库后，需要执行提交操作
                except Exception as e:
                    # 发生错误时回滚
                    print("Error:", e)
                    self.conn.rollback()
