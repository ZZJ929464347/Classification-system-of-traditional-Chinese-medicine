import pymysql

# #连接数据库
# conn=pymysql.connect(host = '127.0.0.1' # 连接名称，默认127.0.0.1 
# ,user = 'root' # 用户名
# ,passwd='root' # 密码
# ,port=3306 # 端口，默认为3306
# ,db='medical' # 数据库名称
# ,charset='utf8' # 字符编码
# )
# cur = conn.cursor() # 生成游标对象 
# sql="select * from Info_table " # SQL语句
# cur.execute(sql) # 执行SQL语句
# data = cur.fetchall() # 通过fetchall方法获得数据
# print(data[0][1])
# cur.close() # 关闭游标
# conn.close() # 关闭连接


class Mysql(object):
    def __init__(self):
        try:
            # 打开数据库连接
            #连接数据库所需的值，可以在__init__()中传入
            self.conn = pymysql.connect(
                host = '127.0.0.1',
                port = 3306,
                user = "root",
                passwd = 'root',
                db = "medical",
                charset = 'utf8'
            )
        except Exception as e:
            print(e)
        else:
            # 使用 cursor() 方法创建一个游标对象 cursor
            self.cur = self.conn.cursor()
            print("连接数据库成功")

    def show(self, name):
        sql = "select * from Info_table where name = '%s'" %name
        try:
            self.cur.execute(sql)
            # fetchall()返回的结果是list，list里面再嵌套list
            res = self.cur.fetchall()
            if res == ():
                print("数据库为空")
                return []
            else:
                name = res[0][0]
                info = res[0][1]
                imgPath = res[0][2]
                return name, info, imgPath
        except  Exception as e:
            print(e + "select data fail")
        else:
            print("查询数据库成功")

    # 关闭数据库连接
    def close(self):
        self.cur.close()
        self.conn.close()
        print("关闭数据库成功")

if __name__ == "__main__":
    mysql = Mysql()
    name, info, imgPath = mysql.show("苍耳子")
    print(imgPath)
    mysql.close()

