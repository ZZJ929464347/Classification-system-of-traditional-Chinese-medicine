import sys
from PyQt5.QtWidgets import *
from ConsumerStackedExampleUi import ConsumerHomePageUi

# 普通用户权限界面
class ConsumerStackedExample(ConsumerHomePageUi):
    def __init__(self, parent=None):
        super(ConsumerStackedExample, self).__init__(parent)
        self.setUpUi()


if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=ConsumerStackedExample()
    demo.show()
    sys.exit(app.exec_())
