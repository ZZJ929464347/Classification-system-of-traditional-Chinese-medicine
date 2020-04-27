from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from CNNnet.predictSingleImg import CNN
from Mysql.DataBase import Mysql
import qtawesome


class ConsumerHomePageUi(QWidget):
    def __init__(self, parent=None):
        super(ConsumerHomePageUi, self).__init__(parent)


    def setUpUi(self):
        #设置窗口初始位置和大小
        self.setGeometry(300,100,1200,800)
        self.setWindowTitle('中药饮片分类系统')
        self.setWindowIcon(QIcon('../source/img/logo.jpg'))

        #创建列表窗口，添加条目
        self.leftlist=QListWidget()
        item3 = QtWidgets.QListWidgetItem(qtawesome.icon('fa.plane', color='white'), '图像预测')
        item4 = QtWidgets.QListWidgetItem(qtawesome.icon('fa.search', color='white'), '中药查询')
        self.leftlist.insertItem(0,item3)
        self.leftlist.insertItem(1,item4)

        #创建四个小控件
        self.stack3=QWidget()
        self.stack4=QWidget()

        self.stack3UI()
        self.stack4UI()

        #在QStackedWidget对象中填充了四个子控件
        self.stack=QStackedWidget(self)
        self.stack.addWidget(self.stack3)
        self.stack.addWidget(self.stack4)

        # 增加比例分割器
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.leftlist)
        splitter.addWidget(self.stack)
        splitter.setStretchFactor(0, 5)
        splitter.setStretchFactor(1, 13)

        #水平布局，添加部件到布局中
        HBox=QHBoxLayout()
        HBox.addWidget(splitter)
        self.setLayout(HBox)

        # 添加信号与槽
        self.leftlist.currentRowChanged.connect(self.display)

        qssStyle = '''
                QListWidget
                {
                    border:1px solid gray;
                    background:	Gray; 
                    outline:0px;
                    border-radius:10px;
                }
                QListWidget::item
                {
                    color:white;
                    height:100px;
                    border:0px solid gray;
                }
                QListWidget::Item:hover{background:skyblue;border-radius:10px;}
                QListWidget::item:selected{background:lightgray; color:red;border-radius:10px;}
                QListWidget::item:selected:!active{border-width:0px; background:lightgreen;border-radius:10px;}
                
                QPushButton{
                    border-radius:10px;
                    background:LightGray;
                    color:black;
                    font-size:13px;
                    height:30px;
                    text-align:center;
                }
                QPushButton:hover{
                    color:black;
                    border:1px solid #F3F3F5;
                    border-radius:10px;
                    background:DarkGray;
                }
                
                QLineEdit{
                    border:1px solid gray;
                    width:300px;
                    border-radius:10px;
                    padding:2px 4px;
                }
                
                QTextEdit{
                   
                    border-radius:20px;
                }
                '''
        # 加载全局的样式
        self.setStyleSheet(qssStyle)
        # 设置背景透明
        self.setWindowOpacity(0.95)
        # self.setWindowFlag(Qt.FramelessWindowHint)


    # 图像预测模块
    def stack3UI(self):

        # 设置栅格布局
        grid3 = QGridLayout()
        grid3.setSpacing(10)

        # 设置加载待分类图片按钮
        buttonChoosePredictImg = QtWidgets.QPushButton(self)
        buttonChoosePredictImg.setObjectName("buttonChoosePredictImg")
        buttonChoosePredictImg.setText("选择待分类图像")
        buttonChoosePredictImg.clicked.connect(self.getPredictImgPath)

        # 设置加载待分类图片编辑框
        self.lineEditChoosePredictImg = QLineEdit()

        grid3.addWidget(buttonChoosePredictImg, 1, 1)
        grid3.addWidget(self.lineEditChoosePredictImg, 1, 2, 1, 7)

        # 显示预测图片的label
        self.predictImageLabel = QLabel(self)
        self.predictImageLabel.setText("                                             显示预测图片")
        self.predictImageLabel.setFixedSize(800, 700)
        self.predictImageLabel.setStyleSheet("QLabel{background:white;}"
                                      "QLabel{color:rgb(300,300,300,120);font-size:10px;font-weight:bold;font-family:宋体;}"
                                      )
        self.predictImageLabel.setStyleSheet(
            '''
            background:	Gainsboro;
            border-radius:40px;
           '''
        )

        # 将预测图片的label加入栅格布局中
        grid3.addWidget(self.predictImageLabel, 3, 2, 6, 5)

        # 设置选择分类网络下拉复选框
        self.netCombobox = QComboBox(self)
        self.netCombobox.setObjectName("netCombobox")
        # 初始化combobox
        self.init_netCombobox()
        grid3.addWidget(self.netCombobox, 9, 2, 1, 1)

        # 设置加载模型按钮
        buttonLoadModel = QtWidgets.QPushButton(self)
        buttonLoadModel.setObjectName("buttonLoadModel")
        buttonLoadModel.setText("加载模型")
        buttonLoadModel.clicked.connect(self.loadModel)
        grid3.addWidget(buttonLoadModel, 9, 3)

        # 设置预测中药图像按钮
        buttonPredictImg = QtWidgets.QPushButton(self)
        buttonPredictImg.setObjectName("buttonPredictImg")
        buttonPredictImg.setText("预测中药图像")
        buttonPredictImg.clicked.connect(self.predictImg)
        grid3.addWidget(buttonPredictImg, 9, 5)

        self.stack3.setLayout(grid3)

    def stack4UI(self):
        # 设置栅格布局
        grid4 = QGridLayout()
        grid4.setSpacing(10)

        # 设置中药搜索按钮
        buttonSearchMedical = QtWidgets.QPushButton(self)
        buttonSearchMedical.setObjectName("buttonSearchMedical")
        buttonSearchMedical.setText("搜索")
        buttonSearchMedical.clicked.connect(self.serchMedical)

        # 设置中药搜索编辑框
        self.lineEditSearchMedical = QLineEdit()
        self.lineEditSearchMedical.setPlaceholderText("请输入中药名称")

        grid4.addWidget(self.lineEditSearchMedical, 1, 1, 1, 7)
        grid4.addWidget(buttonSearchMedical, 1, 8, 1, 1)

        # 显示中药搜索结果图片展示的label
        self.searchResultImageShowLabel = QLabel(self)
        self.searchResultImageShowLabel.setText("               显示搜索结果图片")
        self.searchResultImageShowLabel.setFixedSize(360, 360)
        self.searchResultImageShowLabel.setStyleSheet("QLabel{background:white;}"
                                             "QLabel{color:rgb(300,300,300,120);font-size:10px;font-weight:bold;font-family:宋体;}"
                                             )
        self.searchResultImageShowLabel.setStyleSheet(
            '''
            background:	Gainsboro;
            border-radius:30px;
           '''
        )
        grid4.addWidget(self.searchResultImageShowLabel, 3, 1, 3, 3)

        # 设置中药搜索结果文字展示编辑框
        self.lineEditResultShow = QTextEdit()
        self.lineEditResultShow.setStyleSheet(
            '''
            background:	Gainsboro;
            border-radius:20px;
           '''
        )
        grid4.addWidget(self.lineEditResultShow, 3, 4, 7, 5)

        self.stack4.setLayout(grid4)

    # 槽-----------------------------界面切换
    def display(self,i):
        #设置当前可见的选项卡的索引
        self.stack.setCurrentIndex(i)


    # 槽-----------------------------选择待预测中药图像文件位置
    def getPredictImgPath(self):
        self.getPredictImgPath, _  = QFileDialog.getOpenFileName(self, "选取文件", "./")  # 起始路径
        self.lineEditChoosePredictImg.setText(self.getPredictImgPath)
        print(self.getPredictImgPath)
        jpg = QPixmap(self.getPredictImgPath).scaled(self.predictImageLabel.width(), self.predictImageLabel.height())
        self.predictImageLabel.setPixmap(jpg)


    # 槽-----------------------------加载模型
    def loadModel(self):
        self.cnn = CNN(self.netCombobox.currentIndex())
        self.cnn.loadModel()
        QMessageBox.about(self, "提示", "模型加载成功")


    # 槽-----------------------------预测中药图像
    def predictImg(self):
        result = self.cnn.predict(self.getPredictImgPath)
        QMessageBox.about(self, "提示", "预测结果：" + result)


    # 槽-----------------------------搜索中药
    def serchMedical(self):
        mysql = Mysql()
        result = mysql.show(self.lineEditSearchMedical.text())
        if  result == []:
            QMessageBox.about(self, "提示", "无结果，请重新查询")
        else:
            name, info, imgPath = result
            print(imgPath)
            # 显示搜索的中药图片
            jpg = QPixmap(imgPath).scaled(self.searchResultImageShowLabel.width(),
                                           self.searchResultImageShowLabel.height())
            self.searchResultImageShowLabel.setPixmap(jpg)
            # 显示搜索的中药信息
            self.lineEditResultShow.setText(info)
        mysql.close()


    ####### 初始化netCombobox选择网络的下拉选项框数据  增加单项元素，不带数据  #########
    def init_netCombobox(self):
        items_list = ['vgg16-----0', 'resnet50---1', 'inceptionV3---2']
        for i in range(len(items_list)):
            self.netCombobox.addItem(items_list[i])
        self.netCombobox.setCurrentIndex(0)

