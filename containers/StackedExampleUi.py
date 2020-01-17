import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os
import re
import shutil

class HomePageUi(QWidget):
    def __init__(self, parent=None):
        super(HomePageUi, self).__init__(parent)


    def setUpUi(self):
        #设置窗口初始位置和大小
        self.setGeometry(300,100,1100,800)
        self.setWindowTitle('StackedWidget 例子')

        #创建列表窗口，添加条目
        self.leftlist=QListWidget()
        self.leftlist.insertItem(0,'爬虫')
        self.leftlist.insertItem(1,'图像预处理')
        self.leftlist.insertItem(2,'图像预测')

        #创建三个小控件
        self.stack1=QWidget()
        self.stack2=QWidget()
        self.stack3=QWidget()

        # self.stack1UI()
        self.stack1UI()
        self.stack2UI()
        self.stack3UI()

        #在QStackedWidget对象中填充了三个子控件
        self.stack=QStackedWidget(self)
        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)

        # 增加比例分割器
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.leftlist)
        splitter.addWidget(self.stack)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 13)

        #水平布局，添加部件到布局中
        HBox=QHBoxLayout()
        HBox.addWidget(splitter)
        self.setLayout(HBox)

        # 添加信号与槽
        self.leftlist.currentRowChanged.connect(self.display)


    def stack1UI(self):
        pass


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
        self.imageLabel.setText("                  显示图片")
        self.imageLabel.setFixedSize(800, 700)
        self.imageLabel.setStyleSheet("QLabel{background:white;}"
                                      "QLabel{color:rgb(300,300,300,120);font-size:10px;font-weight:bold;font-family:宋体;}"
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

        # 将垂直布局加入窗体
        self.stack2.setLayout(grid2)


    def stack3UI(self):
        # 水平布局
        layout = QHBoxLayout()

        # 添加控件到布局中
        layout.addWidget(QLabel('科目'))
        layout.addWidget(QCheckBox('物理'))
        layout.addWidget(QCheckBox('高数'))

        self.stack3.setLayout(layout)


    # 槽-----------------------------界面切换
    def display(self,i):
        #设置当前可见的选项卡的索引
        self.stack.setCurrentIndex(i)


    #槽-----------------------------获取预处理图像文件夹
    def getDirectory(self):
        self.getChooseDirectory = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")  # 起始路径
        self.lineEditChooseDirectory.setText(self.getChooseDirectory)
        # 从选取文件夹以后，开始遍历所有的图片，并从list[0]开始遍历图片
        self.imgNumber = 0
        self.imgNameList = self.randomGetImage(self.getChooseDirectory)
        # 获取文件夹里面的图片，并显示到self.imageLabel上
        self.getNewLabelImage()


    # 槽-----------------------------获取保存图像文件夹
    def saveDirectory(self):
        self.getSaveDirectory = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")  # 起始路径
        self.lineEditSaveDirectory.setText(self.getSaveDirectory)
        # 获取保存图像文件夹当前文件的个数
        self.saveDirectoryImgNumber = len(os.listdir(self.getSaveDirectory)) + 1
        print(self.saveDirectoryImgNumber)


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


    # 当点击打标签的多选框选项时，触发事件
    def on_labelCombobox_Activate(self, index):
        if self.imgNumber < len(self.imgNameList):
            suffix = self.get_suffix(self.imageNowPath)
            saveImgPath = self.getSaveDirectory + "/" + str(self.labelCombobox.currentIndex()) + "-" + str(self.saveDirectoryImgNumber) + suffix
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

