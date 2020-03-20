from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os
import re
import shutil
import shlex
import subprocess
from PyQt5.QtCore import QThread, pyqtSignal
from CNNnet.predictSingleImg import CNN
from Mysql.DataBase import Mysql
import qtawesome


class HomePageUi(QWidget):
    def __init__(self, parent=None):
        super(HomePageUi, self).__init__(parent)

    def setUpUi(self):
        # 设置窗口初始位置和大小
        self.setGeometry(300, 100, 1200, 800)
        self.setWindowTitle('中药饮片分类系统')
        self.setWindowIcon(QIcon('../source/img/logo.jpg'))

        # 创建列表窗口，添加条目
        self.leftlist = QListWidget()
        item1 = QtWidgets.QListWidgetItem(qtawesome.icon('fa.sellsy', color='white'), '爬虫功能')
        item2 = QtWidgets.QListWidgetItem(qtawesome.icon('fa.hand-o-right', color='white'), '图像处理')
        item3 = QtWidgets.QListWidgetItem(qtawesome.icon('fa.plane', color='white'), '图像预测')
        item4 = QtWidgets.QListWidgetItem(qtawesome.icon('fa.search', color='white'), '中药查询')
        self.leftlist.insertItem(0, item1)
        self.leftlist.insertItem(1, item2)
        self.leftlist.insertItem(2, item3)
        self.leftlist.insertItem(3, item4)

        # 创建四个小控件
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()

        # self.stack1UI()
        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.stack4UI()

        # 在QStackedWidget对象中填充了四个子控件
        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)
        self.stack.addWidget(self.stack4)

        # 增加比例分割器
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.leftlist)
        splitter.addWidget(self.stack)
        splitter.setStretchFactor(0, 5)
        splitter.setStretchFactor(1, 13)

        # 水平布局，添加部件到布局中
        HBox = QHBoxLayout()
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

    def stack1UI(self):
        # 设置栅格布局
        grid1 = QGridLayout()
        grid1.setSpacing(10)

        # 设置搜索中药饮片名称label
        self.searchNameLabel = QLabel(self)
        self.searchNameLabel.setText("中药饮片名称：")
        grid1.addWidget(self.searchNameLabel, 1, 1, 1, 1)

        # 设置图片保存目录位置label
        self.spiderSaveDirectory = QLabel(self)
        self.spiderSaveDirectory.setText("图片保存目录位置：")
        grid1.addWidget(self.spiderSaveDirectory, 3, 1, 1, 1)

        # 设置搜索的开始爬取页数label
        self.searchStartPageLabel = QLabel(self)
        self.searchStartPageLabel.setText("开始页数：")
        grid1.addWidget(self.searchStartPageLabel, 5, 1, 1, 1)

        # 设置需要搜索的爬取页数label
        self.searchCountLabel = QLabel(self)
        self.searchCountLabel.setText("搜索页数：")
        grid1.addWidget(self.searchCountLabel, 7, 1, 1, 1)

        # 设置进度显示Text
        self.spiderInfo = QTextEdit()
        self.spiderInfo.setStyleSheet(
            '''
            background:	Gainsboro;
            border-radius:20px;
           '''
        )
        grid1.addWidget(self.spiderInfo, 1, 8, 20, 4)

        # 设置搜索中药饮片名称输入框
        self.lineEditSearchName = QLineEdit()
        grid1.addWidget(self.lineEditSearchName, 1, 2, 1, 5)

        # 设置图片保存目录位置的输入框
        self.lineEditSpiderSaveDirectory = QLineEdit()
        grid1.addWidget(self.lineEditSpiderSaveDirectory, 3, 2, 1, 4)

        # 设置搜索的开始爬取页数输入框
        self.lineEditStartPage = QLineEdit()
        grid1.addWidget(self.lineEditStartPage, 5, 2, 1, 2)

        # 设置需要搜索的爬取页数输入框
        self.lineEditSearchCount = QLineEdit()
        grid1.addWidget(self.lineEditSearchCount, 7, 2, 1, 2)

        # 设置选取爬虫模块图像文件夹保存目录按钮1
        buttonSpiderSaveDirectory = QPushButton(self)
        buttonSpiderSaveDirectory.setObjectName("buttonSpiderSaveDirectory")
        buttonSpiderSaveDirectory.setText("选择保存目录")
        buttonSpiderSaveDirectory.clicked.connect(self.getSpiderSaveDirectory)
        grid1.addWidget(buttonSpiderSaveDirectory, 3, 6, 1, 1)

        # 设置开始爬取按钮1
        self.buttonStartSpider = QPushButton(self)
        self.buttonStartSpider.setObjectName("buttonStartSpider")
        self.buttonStartSpider.setText("开始爬取")
        self.buttonStartSpider.clicked.connect(self.startSpider)
        grid1.addWidget(self.buttonStartSpider, 18, 2, 1, 4)

        # 将栅格布局加入窗体
        self.stack1.setLayout(grid1)

    # 图像预处理模块
    def stack2UI(self):
        # 设置加载预处理图像文件夹按钮1
        buttonChooseDirectory = QtWidgets.QPushButton(self)
        buttonChooseDirectory.setObjectName("buttonChooseDirectory")
        buttonChooseDirectory.setText("预处理图像文件夹")
        buttonChooseDirectory.clicked.connect(self.getDirectory)
        # 设置保存预处理图像文件夹按钮2
        buttonSaveDirectory = QtWidgets.QPushButton(self)
        buttonSaveDirectory.setObjectName("buttonSaveDirectory")
        buttonSaveDirectory.setText("保存图像文件夹")
        buttonSaveDirectory.clicked.connect(self.saveDirectory)

        # 设置获取预处理图像文件夹位置编辑框1
        self.lineEditChooseDirectory = QLineEdit()
        # 设置获取保存图像文件夹位置编辑框2
        self.lineEditSaveDirectory = QLineEdit()

        # 设置栅格布局
        grid2 = QGridLayout()
        grid2.setSpacing(10)

        grid2.addWidget(buttonChooseDirectory, 1, 1)
        grid2.addWidget(self.lineEditChooseDirectory, 1, 2, 1, 7)

        grid2.addWidget(buttonSaveDirectory, 2, 1)
        grid2.addWidget(self.lineEditSaveDirectory, 2, 2, 1, 7)

        # 显示图片的label
        self.imageLabel = QLabel(self)
        self.imageLabel.setText("                                               显示图片")
        self.imageLabel.setFixedSize(800, 700)
        self.imageLabel.setStyleSheet("QLabel{background:white;}"
                                      "QLabel{color:rgb(300,300,300,120);font-size:10px;font-weight:bold;font-family:宋体;}"
                                      )
        self.imageLabel.setStyleSheet(
            '''
            background:	Gainsboro;
            border-radius:40px;
           '''
        )

        # 将图片的label加入栅格布局中
        grid2.addWidget(self.imageLabel, 3, 2, 6, 5)

        # 下一张图片按钮
        buttonNextImage = QPushButton(self)
        buttonNextImage.setObjectName("buttonNextImage")
        buttonNextImage.setText("下一张图像")
        buttonNextImage.clicked.connect(self.nextImgFile)
        grid2.addWidget(buttonNextImage, 10, 2, 1, 1)

        # 设置删除图像按钮
        buttonDelImage = QPushButton(self)
        buttonDelImage.setObjectName("buttonDelImage")
        buttonDelImage.setText("删除图像")
        buttonDelImage.clicked.connect(self.delFile)
        grid2.addWidget(buttonDelImage, 10, 4, 1, 1)

        # 设置打标签图像下拉复选框
        self.labelCombobox = QComboBox(self)
        self.labelCombobox.setObjectName("labelCombobox")
        # 初始化combobox
        self.init_labelCombobox()
        # 增加选中事件
        self.labelCombobox.activated.connect(self.on_labelCombobox_Activate)
        grid2.addWidget(self.labelCombobox, 10, 6, 1, 1)

        # 将栅格布局加入窗体
        self.stack2.setLayout(grid2)

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
    def display(self, i):
        # 设置当前可见的选项卡的索引
        self.stack.setCurrentIndex(i)

    # 槽-----------------------------选择爬虫保存图像文件夹
    def getSpiderSaveDirectory(self):
        self.getSpiderSaveDirectoryPath = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")  # 起始路径
        self.lineEditSpiderSaveDirectory.setText(self.getSpiderSaveDirectoryPath)

    # 槽-----------------------------获取预处理图像文件夹
    def getDirectory(self):
        self.getChooseDirectory = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")  # 起始路径
        self.lineEditChooseDirectory.setText(self.getChooseDirectory)
        # 从选取文件夹以后，开始遍历所有的图片，并从list[0]开始遍历图片
        self.imgNumber = 0
        try:
            self.imgNameList = self.randomGetImage(self.getChooseDirectory)
            # 获取文件夹里面的图片，并显示到self.imageLabel上
            self.getNewLabelImage()
        except:
            print("预处理图像文件夹为空")

    # 槽-----------------------------获取保存图像文件夹
    def saveDirectory(self):
        self.getSaveDirectory = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")  # 起始路径
        self.lineEditSaveDirectory.setText(self.getSaveDirectory)
        # 获取保存图像文件夹当前文件的个数
        try:
            self.saveDirectoryImgNumber = len(os.listdir(self.getSaveDirectory)) + 1
            print(self.saveDirectoryImgNumber)
        except:
            print("保存图像文件夹为空")

    # 槽-----------------------------选择待预测中药图像文件位置
    def getPredictImgPath(self):
        self.getPredictImgPath, _ = QFileDialog.getOpenFileName(self, "选取文件", "./")  # 起始路径
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
        if result == []:
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

    # 槽-----------------------------点击爬虫按钮，开始爬取
    def startSpider(self):
        medicineName = self.lineEditSearchName.text()
        medicineStart_page = self.lineEditStartPage.text()
        medicineSpider_page_num = self.lineEditSearchCount.text()
        saveDirectoryPath = self.lineEditSpiderSaveDirectory.text()

        # 使用创建好的爬虫运行进程执行，避免父进程出现假死现象
        self.thread_1 = ThreadCrawl(medicineName, medicineStart_page, medicineSpider_page_num, saveDirectoryPath)
        # thread_1的trigger与槽print_in_textEdit连接，方便在子线程内直接发射信号
        self.thread_1.trigger.connect(self.print_in_textEdit)
        self.thread_1.start()

    # 将爬虫的控制台信息显示在spiderInfo控件上
    def print_in_textEdit(self, msg):
        self.spiderInfo.append(msg)
        self.thread_1.exit()

    # 从文件夹中获取图像文件名称，但是不是有序的
    def randomGetImage(self, directoryPath):
        result = os.listdir(directoryPath)
        return result

    # 获取下一张图片
    def nextImgFile(self):
        self.imgNumber = self.imgNumber + 1
        self.getNewLabelImage()

    # 获取文件夹里面的图片，并显示到self.imageLabel上
    def getNewLabelImage(self):
        if self.imgNumber < len(self.imgNameList):
            self.imageNowPath = self.getChooseDirectory + "/" + self.imgNameList[self.imgNumber]
            jpg = QPixmap(self.imageNowPath).scaled(self.imageLabel.width(), self.imageLabel.height())
            self.imageLabel.setPixmap(jpg)
        else:
            print("已经到最后一张图片了")
        # print(self.imagePath)
        # print(self.getChooseDirectory)

    # 删除文件
    def delFile(self):
        if os.path.exists(self.imageNowPath):  # 如果文件存在
            # 删除文件
            os.remove(self.imageNowPath)
            self.imgNumber = self.imgNumber + 1
            # 获取文件夹里面的图片，并显示到self.imageLabel上
            self.getNewLabelImage()
        else:
            print('no such file:%s' % self.imageNowPath)

    ####### 初始化labelCombobox打标签的下拉选项框数据  增加单项元素，不带数据  #########
    def init_labelCombobox(self):
        items_list = ['苍术-----0', '苍耳子---1', '决明子---2', '枳实-----3', '天花粉---4', '黄连-----5']
        for i in range(len(items_list)):
            self.labelCombobox.addItem(items_list[i])
        self.labelCombobox.setCurrentIndex(-1)

    ####### 初始化netCombobox选择网络的下拉选项框数据  增加单项元素，不带数据  #########
    def init_netCombobox(self):
        items_list = ['vgg16-----0', 'resnet50---1', 'inceptionV3---2']
        for i in range(len(items_list)):
            self.netCombobox.addItem(items_list[i])
        self.netCombobox.setCurrentIndex(0)

    # 当点击打标签的多选框选项时，触发事件
    def on_labelCombobox_Activate(self, index):
        if self.imgNumber < len(self.imgNameList):
            suffix = self.get_suffix(self.imageNowPath)
            saveImgPath = self.getSaveDirectory + "/" + str(self.labelCombobox.currentIndex()) + "-" + str(
                self.saveDirectoryImgNumber) + suffix
            # 移动图片文件
            shutil.move(self.imageNowPath, saveImgPath)
            # 保存文件夹数+1
            self.saveDirectoryImgNumber = self.saveDirectoryImgNumber + 1
            # 当前展示的图片+1
            self.imgNumber = self.imgNumber + 1
            # 获取文件夹里面的图片，并显示到self.imageLabel上
            self.getNewLabelImage()
        else:
            print("已经到最后一张图片了")
        # print("saveImgPath:" + saveImgPath)
        # print(self.labelCombobox.currentIndex())
        # print(self.labelCombobox.currentText())

    # 获取后缀名
    def get_suffix(self, name):
        # \.是匹配.的意思 ^\.是匹配不是.的字符 [^\.]是匹配任意不是.的字符当中的一个   [^\.]*匹配0个或任意多个不是.的字符  匹配到$结束符    search方法扫描整个字符串并返回第一个成功的匹配
        m = re.search(r'\.[^\.]*$', name)
        # print("m为：" + str(m))
        # group(0)就是指匹配的完整字符串  group(1)是指串中串
        if m.group(0) and len(m.group(0)) <= 5:
            return m.group(0)
        else:
            return '.jpeg'


# 设置一个线程，用来实时显示爬虫的最新信息
class ThreadCrawl(QThread):
    trigger = pyqtSignal(str)

    def __init__(self, name, spider_page_num, start_page, saveDirectoryPath):
        super(ThreadCrawl, self).__init__()
        self.name = name
        self.spider_page_num = spider_page_num
        self.start_page = start_page
        self.saveDirectoryPath = saveDirectoryPath

    def run(self):
        shell_cmd = "python ../爬虫.py" + " " + str(self.name) + " " + str(self.spider_page_num) + " " + str(
            self.start_page) + " " + str(self.saveDirectoryPath)
        cmd = shlex.split(shell_cmd)
        p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while p.poll() is None:
            line = p.stdout.readline().decode("UTF-8")
            line = line.strip()
            if line:
                self.trigger.emit(str(line))


