import pymysql


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


    # 搜索中药信息
    def show(self, name):
        sql = "select * from info_table where name = '%s'" %name
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


    # 注册新的消费者用户
    def AddConsumer(self, consumerAccount, consumerPassword):
        sql = "INSERT INTO consumerInfo_table (consumerAccount, consumerPassword) VALUES ('%s','%s')"%(consumerAccount,consumerPassword)
        try:
            self.cur.execute(sql)
            self.conn.commit()
            print("消费者信息注册成功")
        except  Exception as e:
            print(e + "insert consumerAccount fail")


    # 判断是否存在消费者账户 如果存在返回exist  不存在返回notExist
    def ifExistConsumerAccount(self, consumerAccount):
        sql =  "select * from consumerInfo_table where consumerAccount = '%s'" %consumerAccount
        try:
            self.cur.execute(sql)
            res = self.cur.fetchall()
            if res == ():
                print("不存在该消费者账户")
                return "notExist"
            else:
                print("请更改")
                return "exist"
        except  Exception as e:
            print(e)


    # 判断消费者账号、密码是否正确 正确返回true 错误返回false
    def ifTrueConsumer(self, consumerAccount, consumerPassword):
        sql = "select * from consumerInfo_table where consumerAccount = '%s' and consumerPassword = '%s'" % (consumerAccount, consumerPassword)
        try:
            self.cur.execute(sql)
            res = self.cur.fetchall()
            if res == ():
                print("消费者账号密码错误")
                return "false"
            else:
                print("消费者账号密码正确")
                return "true"
        except  Exception as e:
            print(e)




    # 判断管理员账号、密码是否正确 正确返回true 错误返回false
    def ifTrueAdmin(self, adminAccount, adminPassword):
        sql =  "select * from adminInfo_table where adminAccount = '%s' and adminPassword = '%s'" %(adminAccount, adminPassword)
        try:
            self.cur.execute(sql)
            res = self.cur.fetchall()
            if res == ():
                print("管理员账号密码错误")
                return "false"
            else:
                print("管理员账号密码正确")
                return "true"
        except  Exception as e:
            print(e)


    # 关闭数据库连接
    def close(self):
        self.cur.close()
        self.conn.close()
        print("关闭数据库成功")


if __name__ == "__main__":
    mysql = Mysql()
    # name, info, imgPath = mysql.show("苍耳子")
    # print(imgPath)

    # # 插入消费者账号
    # mysql.AddConsumer("zzz123213","6666666")

    # ##判断管理员账号、密码是否正确
    # result = mysql.ifTrueAdmin("123","456")
    # print(result)

    # #判断消费者账号、密码是否正确
    result = mysql.ifTrueConsumer("1234","5678")
    print(result)

    mysql.close()

