
from PyQt5 import QtGui, QtWidgets
import sys, os
from PyQt5.QtWidgets import *
from gui import Ui_MainWindow

basedir = os.path.dirname(__file__)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, "icons", "unnamed.png")))

    # app.setWindowIcon(QtGui.QIcon('icons/unnamed.png'))
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    MainWindow.show()
    sys.exit(app.exec_())