import sys
from PyQt5.QtWidgets import *
from StackedExampleUi import HomePageUi

# HomePageUi是第一个主界面
class StackedExample(HomePageUi):
    def __init__(self, parent=None):
        super(StackedExample, self).__init__(parent)
        self.setUpUi()


if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=StackedExample()
    demo.show()
    sys.exit(app.exec_())
