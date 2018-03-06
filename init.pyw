import sys

from PyQt5 import QtWidgets

from mainUI import MainWindow

"""程序启动器"""
if __name__ == '__main__':
    argv = sys.argv
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())
