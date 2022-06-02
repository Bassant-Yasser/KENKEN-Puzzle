from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from kenken_algorithms import gather
from kenken_helper import  Kenken_Board
from table import TableModel

from random import randint
class Ui_MainWindow(object):
    alg_choice = ""
    size_choice = 0
    gen_flag = False
    output_file = ""
    assignment = []
    data = [["Algorithm", "Size","Checks", "Assignments", "Time"]]
    groups = []
    w_list = []
    row = []
    Kgenerator = Kenken_Board(0)

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(1397, 807)
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.size_box = QtWidgets.QSpinBox(self.centralwidget)
        self.size_box.setGeometry(QtCore.QRect(110, 40, 52, 30))
        self.size_box.setMinimum(3)
        self.size_box.setMaximum(9)
        self.size_box.setObjectName("size_box")
        self.alg = QtWidgets.QComboBox(self.centralwidget)
        self.alg.setGeometry(QtCore.QRect(110, 90, 100, 29))
        self.alg.setObjectName("alg")
        
        self.gen = QtWidgets.QPushButton(self.centralwidget)
        self.gen.setGeometry(QtCore.QRect(70, 130, 106, 30))
        self.gen.setObjectName("gen")
        self.solve = QtWidgets.QPushButton(self.centralwidget)
        self.solve.setGeometry(QtCore.QRect(190, 130, 106, 30))
        self.solve.setObjectName("solve")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(310, 130, 106, 30))
        self.pushButton.setObjectName("clear")


        
        self.smode = QtWidgets.QPushButton('multi test',self.centralwidget)
        self.smode.setCheckable(True)
        self.smode.setGeometry(QtCore.QRect(70, 180, 106, 30))
        self.smode.clicked[bool].connect(self.switchmode)
        self.label_performance = QtWidgets.QLabel(self.centralwidget)
        self.label_performance.setGeometry(QtCore.QRect(200, 155, 120, 100))
        self.label_performance.setObjectName("label_performance")
        self.label_performance.setText("")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 40, 80, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 100, 21))
        self.label_2.setObjectName("label_2")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(550, 100, 871, 800))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(5, 271, 520, 380))
        self.tableView.setObjectName("tableView")

        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1397, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)
        self.actionsave_result_as_csv = QtWidgets.QAction(self.MainWindow)
        self.actionsave_result_as_csv.setObjectName("actionsave_result_as_csv")
        self.actionsave_result_as_csv.triggered.connect(self.save_csv)
        self.actionsave_result_as_csv.setDisabled(True)
        self.actionsave_result_as_txt = QtWidgets.QAction(self.MainWindow)
        self.actionsave_result_as_txt.setObjectName("actionsave_result_as_txt")
        self.actionsave_result_as_txt.triggered.connect(self.save_txt)
        self.actionsave_result_as_txt.setDisabled(True)
        self.menuFile.addAction(self.actionsave_result_as_csv)
        self.menuFile.addAction(self.actionsave_result_as_txt)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(self.MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
        
    def switchmode(self):
        if self.smode.isChecked():
            # file_name = QFileDialog.getSaveFileName(self.MainWindow, 'Save File', '', 'CSV(*.csv)')
            with open("test.csv", 'w') as f:
                # for row in self.tableView.model()._data:
                #     f.write(','.join(str(col) for col in row) + '\n')
                data = ["Algorithm", "Size","Checks", "Assignments", "Time"]
                f.write(','.join(str(col) for col in data) + '\n')
                BT_t = 0
                FC_t = 0
                MAC_t = 0
                for i in range(0,35):
                    size = randint(3,6)
                    self.Kgenerator.change_size(size)
                    Gboard = self.Kgenerator.Generate_groups()
                    t = Gboard
                    a, data = gather("BT", size, t)
                    data = ["BT", size, data[0], data[1], data[2]]
                    f.write(','.join(str(col) for col in data) + '\n')
                    BT_t += data[4]
                    t = Gboard
                    _, data = gather("BT+FC", size, t)
                    data = ["BT+FC", size, data[0], data[1], data[2]]
                    f.write(','.join(str(col) for col in data) + '\n')
                    FC_t += data[4]
                    t = Gboard
                    _, data = gather("BT+MAC", size, t)
                    data = ["BT+MAC", size, data[0], data[1], data[2]]
                    f.write(','.join(str(col) for col in data) + '\n')
                    MAC_t += data[4]
                perf="BT: "+ str(BT_t)+"\n FC: "+str(FC_t)+"\n MAC: "+str(MAC_t)
                self.label_performance.setText(perf)
                self.smode.setChecked(False)
                  
    def save_csv(self):
        file_name = QFileDialog.getSaveFileName(self.MainWindow, 'Save File', '', 'CSV(*.csv)')
        with open(file_name[0], 'w') as f:
            for row in self.tableView.model()._data:
                f.write(','.join(str(col) for col in row) + '\n')
    def save_txt(self):
        file_name = QFileDialog.getSaveFileName(self.MainWindow, 'Save File', '', 'TXT(*.txt)')
        with open(file_name[0], 'w') as f:
            for row in self.tableView.model()._data:
                f.write(','.join(str(col) for col in row) + '\n')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Kenken"))
        self.gen.setText(_translate("MainWindow", "Generate"))
        self.solve.setText(_translate("MainWindow", "Solve"))
        self.label.setText(_translate("MainWindow", "Solve: "))
        self.label_2.setText(_translate("MainWindow", "Algorithm: "))
        self.alg.addItems(["BT", "BT+FC", "BT+MAC"])
        self.alg.activated[str].connect(self.onChanged)
        self.size_box.valueChanged.connect(self.onSizeChanged)
        self.pushButton.setText(_translate("MainWindow", "Clear"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionsave_result_as_csv.setText(_translate("MainWindow", "save result as csv"))
        self.actionsave_result_as_txt.setText(_translate("MainWindow", "save result as txt"))
        # self.actionsave_result_as_csv.triggered.connect(self.save_result_as_csv)
        # self.actionsave_result_as_txt.triggered.connect(self.save_result_as_txt)
        self.size_choice = self.size_box.value()
        self.alg_choice = self.alg.currentText()
        self.solve.clicked.connect(self.solve_clicked)
        self.gen.clicked.connect(self.gen_clicked)
        self.pushButton.clicked.connect(self.clear_b)

        self.solve.setDisabled(True)
        MainWindow.showMaximized()
    

    def add_grid_gen(self, groups):
        # colors = ["green", "blue", "red", "yellow", "black", "orange", "violet", "brown", "pink", "grey", "DodgerBlue", "Tomato", "Lime", "Cyan", "Magenta", "DarkRed", "DarkGreen", "DarkBlue", "DarkCyan", "DarkMagenta", "DarkYellow", "DarkGray", "LightGray", "MidnightBlue", "Navy", "Olive", "Purple", "Teal", "Maroon", "LawnGreen", "Aqua", "Fuchsia", "Red", "Green", "Blue", "Cyan", "Magenta", "Yellow", "Gray", "White"]
        colors = ['blue', 'Cyan', 'DarkGreen', 'black', 'DarkCyan', 'DarkGray', 'MidnightBlue', 'Maroon', 'DarkRed', 'red', 'yellow', 'DarkYellow', 'Fuchsia', 'Blue', 'DarkMagenta', 'brown', 'green', 'Red', 'orange', 'LawnGreen', 'Green', 'DarkBlue', 'Lime', 'Yellow', 'Aqua', 'Tomato', 'LightGray', 'Purple', 'Navy', 'grey', 'Magenta', 'violet', 'Cyan', 'Gray', 'Magenta', 'pink', 'DodgerBlue', 'Teal', 'White', 'Olive']
        for count, a in enumerate(groups):
            g_color = colors[count%len(colors)]#random.choice(colors)
            op = a[-2]
            num = a[-1]
            t = a[0]
            for itt in range(len(t)):
                if itt == 0:
                    if(op == '.'):
                        w = QtWidgets.QTextEdit(str(num))
                        w.setStyleSheet("background-color: white; color: black;border: 2px solid %s" % g_color)
                    else:
                        w = QtWidgets.QTextEdit(str(num)+ "   " + str(op))
                        w.setStyleSheet("background-color: white; color: black;border: 2px solid %s" % g_color)

                else:
                    w = QtWidgets.QTextEdit(" ")
                    w.setStyleSheet("background-color: white; color: black;border: 2px solid %s" % g_color)
                    w.append(" ")
                w.setReadOnly(True)
                w.setDisabled(True)
                x,y = t[itt][0], t[itt][1]
                self.w_list.append((w, x, y))
                self.gridLayout.addWidget(w, y, x)
    
    
    def add_grid_solve(self, assignment, groups):
        for a in groups:
            t = a[0]
            result = 0
            list = ()
            for key ,b in assignment.items():
                if key == a[0]:
                    list = b
                    del assignment[key]
                    break
    
            for itt in range(len(t)):
                for i in list:
                    result = i
                    list = list[1:]
                    break

                for a in self.w_list:
                    w, x, y= a[0], a[1], a[2]
                    # w.append(" ")
                    w.append("      " + str(result))
                    self.gridLayout.addWidget(w, y, x)
                    self.w_list.remove(a)
                    break
                    # w.setGeometry(QtCore.QRect(y, x, 70, 70))    

    def gen_table(self, data, flag):
        if flag == True:
            d = [[]]
            model = TableModel(d)
            self.tableView.setModel(model)
            return
        d = [self.alg_choice, self.size_choice]
        d = d + list(data)
        self.data.append(list(d))
        model = TableModel(self.data)
        self.tableView.setModel(model)


    def solve_clicked(self):
        self.assignment, self.row = gather(self.alg_choice, self.size_choice, self.groups)

        self.add_grid_solve(self.assignment, self.groups)
        self.gen_table(self.row, False)
        self.solve.setDisabled(True)
        self.actionsave_result_as_csv.setDisabled(False)
        self.actionsave_result_as_txt.setDisabled(False)
    
    def gen_clicked(self):
        self.size_choice = self.size_box.value()
        self.gridLayoutWidget.resize(self.size_choice*80, self.size_choice*80)
        self.alg_choice = self.alg.currentText()
        
        for i in reversed(range(self.gridLayout.count())): 
            self.gridLayout.itemAt(i).widget().deleteLater()
        self.w_list = []
        self.Kgenerator.change_size(self.size_choice)
        self.groups = self.Kgenerator.Generate_groups()
        self.gen_flag = True
        self.add_grid_gen(self.groups)
        self.solve.setDisabled(False)

    def onChanged(self, text):
        self.alg_choice = text 
        if self.gen_flag == True:
            self.solve.setDisabled(False)
        
    def onSizeChanged(self, value):
        self.size_choice = value

    def clear_b(self):
        self.label_performance.setText("")
        self.actionsave_result_as_csv.setDisabled(True)
        self.actionsave_result_as_txt.setDisabled(True)
        for i in reversed(range(self.gridLayout.count())): 
            self.gridLayout.itemAt(i).widget().deleteLater()
        self.w_list = []
        self.data = [["Algorithm", "Size", "Checks", "Assignments", "Time"]]
        self.gen_flag = False
        self.solve.setDisabled(True)
        self.row = []
        self.assignment = {}
        self.groups = []
        self.output_file = ""
        self.alg_choice = ""
        self.size_choice = ""
        self.gen_table(self.row, True)


