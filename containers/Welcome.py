import sys
from PyQt5 import QtGui,QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AdminStackedExampleUi import AdminHomePageUi
from ConsumerStackedExampleUi import ConsumerHomePageUi
from Mysql.DataBase import Mysql

class WelcomeUi(QWidget):
    def __init__(self, parent=None):
        super(WelcomeUi, self).__init__(parent)
        self.setWindowTitle("欢迎界面")
        self.setWindowIcon(QIcon('../source/img/logo.jpg'))
        self.setGeometry(400, 150, 1200, 760)
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(),  QtGui.QBrush(QtGui.QPixmap("../source/img/backgroundImage.jpg")))
        self.setPalette(window_pale)
        # self.setWindowFlags(Qt.FramelessWindowHint)无边框
        self.setFixedSize(self.width(), self.height())

        # 设置账号label
        self.account = QLabel(self)
        self.account.setText("账号：")
        self.account.move(950,550)

        # 设置账号输入框
        self.lineEditAccount = QLineEdit(self)
        self.lineEditAccount.move(1010,546)
        self.lineEditAccount.resize(160,25)
        self.lineEditAccount.setPlaceholderText("请输入账号")

        # 设置密码label
        self.password = QLabel(self)
        self.password.setText("密码：")
        self.password.move(950, 600)

        # 设置密码输入框
        self.lineEditPassword = QLineEdit(self)
        self.lineEditPassword.move(1010,596)
        self.lineEditPassword.resize(160, 25)
        self.lineEditPassword.setEchoMode(QLineEdit.Password)
        self.lineEditPassword.setPlaceholderText("请输入密码")


        # 设置消费者和管理员复选按钮
        self.radioButtonConsumer = QtWidgets.QRadioButton(self)
        self.radioButtonConsumer.move(980,640)
        self.radioButtonConsumer.setText("用户")


        self.radioButtonAdmin = QtWidgets.QRadioButton(self)
        self.radioButtonAdmin.move(1080, 640)
        self.radioButtonAdmin.setText("管理员")

        # 登录按钮
        self.buttonDengLu = QPushButton(self)
        self.buttonDengLu.setText("登录")
        self.buttonDengLu.move(950,670)
        self.buttonDengLu.clicked.connect(self.login)

        # 注册按钮
        self.buttonZhuCe = QPushButton(self)
        self.buttonZhuCe.setText("注册")
        self.buttonZhuCe.move(1080, 670)
        self.buttonZhuCe.clicked.connect(self.register)

        # 登录时进行账号、密码输入校验
        regx = QRegExp("^[a-zA-Z0-9A-Za-z]{14}$")
        validator1 = QRegExpValidator(regx, self.lineEditAccount)
        validator2 = QRegExpValidator(regx, self.lineEditPassword)
        self.lineEditPassword.setValidator(validator1)
        self.lineEditAccount.setValidator(validator2)



    # 用户登录账号、密码检验
    def login(self):
        account = self.lineEditAccount.text()
        password = self.lineEditPassword.text()
        mysql = Mysql()

        # 如果消费者复选按钮被点击
        if self.radioButtonConsumer.isChecked():
            # 判断数据库中是否存在该消费者
            result = mysql.ifTrueConsumer(account, password)
            if result == "true":
                print("密码正确")
                # 关闭登录界面
                self.close()
                # 进入消费者主页面
                consumerHomePage.show()
            else:
                # print("密码错误")
                QMessageBox.about(self, "提示", "账号或密码错误")

        if self.radioButtonAdmin.isChecked():
            # 判断数据库中是否存在该管理员
            result = mysql.ifTrueAdmin(account, password)
            if result == "true":
                print("密码正确")
                # 关闭登录界面
                self.close()
                # 进入管理员主页面
                adminHomePage.show()
            else:
                # print("密码错误")
                QMessageBox.about(self, "提示", "账号或密码错误")
        mysql.close()

    # 注册账号
    def register(self):
        # 展示注册界面UI
        registerDialog.show()


# 注册弹窗UI
class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super(RegisterDialog, self).__init__(parent)
        self.setWindowTitle("注册")
        self.resize(300, 200)

        usr = QLabel("账号：")
        pwd = QLabel("密码：")
        self.usrLineEdit = QLineEdit()
        self.pwdLineEdit = QLineEdit()

        # 注册时进行账号、密码输入校验
        regx = QRegExp("^[a-zA-Z0-9A-Za-z]{14}$")
        validator1 = QRegExpValidator(regx, self.usrLineEdit)
        validator2 = QRegExpValidator(regx, self.pwdLineEdit)
        self.usrLineEdit.setValidator(validator1)
        self.pwdLineEdit.setValidator(validator2)

        gridLayout = QGridLayout()
        gridLayout.addWidget(usr, 0, 0, 1, 1)
        gridLayout.addWidget(pwd, 1, 0, 1, 1)
        gridLayout.addWidget(self.usrLineEdit, 0, 1, 1, 3);
        gridLayout.addWidget(self.pwdLineEdit, 1, 1, 1, 3);

        okBtn = QPushButton("确定")
        cancelBtn = QPushButton("取消")

        btnLayout = QHBoxLayout()
        btnLayout.setSpacing(60)
        btnLayout.addWidget(okBtn)
        btnLayout.addWidget(cancelBtn)

        dlgLayout = QVBoxLayout()
        dlgLayout.setContentsMargins(40, 40, 40, 40)
        dlgLayout.addLayout(gridLayout)
        dlgLayout.addStretch(40)
        dlgLayout.addLayout(btnLayout)

        self.setLayout(dlgLayout)
        # 注册按钮信号
        okBtn.clicked.connect(self.accept)
        # 拒绝按钮信号
        cancelBtn.clicked.connect(self.reject)


    # 注册时检查账号和密码是否在数据库重复
    def accept(self):
        account = self.usrLineEdit.text()
        password = self.pwdLineEdit.text()

        mysql = Mysql()
        result = mysql.ifExistConsumerAccount(account)
        if result == "exist":
            QMessageBox.about(self, "提示", "账号已存在")
        if result == "notExist":
            mysql.AddConsumer(account,password)
            QMessageBox.about(self, "提示", "注册成功")
        mysql.close()

        self.usrLineEdit.setText("")
        self.pwdLineEdit.setText("")
        self.close()


# 管理员权限界面
class AdminStackedExample(AdminHomePageUi):
    def __init__(self, parent=None):
        super(AdminStackedExample, self).__init__(parent)
        self.setUpUi()


# 普通用户权限界面
class ConsumerStackedExample(ConsumerHomePageUi):
    def __init__(self, parent=None):
        super(ConsumerStackedExample, self).__init__(parent)
        self.setUpUi()




if __name__ == '__main__':
    app=QApplication(sys.argv)
    # 登录界面
    welcomeUi=WelcomeUi()
    welcomeUi.show()
    # 注册界面
    registerDialog = RegisterDialog()
    # 登录成功,进入主界面
    adminHomePage = AdminStackedExample()
    consumerHomePage = ConsumerStackedExample()
    sys.exit(app.exec_())


