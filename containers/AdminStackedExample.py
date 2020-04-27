import sys
from PyQt5.QtWidgets import *
from AdminStackedExampleUi import HomePageUi

# HomePageUi是第一个主界面
class AdminStackedExample(HomePageUi):
    def __init__(self, parent=None):
        super(AdminStackedExample, self).__init__(parent)
        self.setUpUi()


if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=AdminStackedExample()
    demo.show()
    sys.exit(app.exec_())
