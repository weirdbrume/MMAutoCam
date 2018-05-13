# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MMAutoCam.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(547, 99)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/icon/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.gridLayout.addWidget(self.lineEdit_1, 0, 0, 1, 4)
        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setObjectName("pushButton_1")
        self.gridLayout.addWidget(self.pushButton_1, 0, 4, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 0, 1, 4)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 4, 1, 1)
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setObjectName("label_1")
        self.gridLayout.addWidget(self.label_1, 2, 0, 1, 1)
        self.doubleSpinBox_1 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_1.setDecimals(0)
        self.doubleSpinBox_1.setMinimum(1.0)
        self.doubleSpinBox_1.setMaximum(3.0)
        self.doubleSpinBox_1.setProperty("value", 1.0)
        self.doubleSpinBox_1.setObjectName("doubleSpinBox_1")
        self.gridLayout.addWidget(self.doubleSpinBox_1, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 2, 1, 1)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_2.setDecimals(0)
        self.doubleSpinBox_2.setMinimum(1.0)
        self.doubleSpinBox_2.setProperty("value", 10.0)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.gridLayout.addWidget(self.doubleSpinBox_2, 2, 3, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 2, 4, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MMAutoCam"))
        self.pushButton_1.setToolTip(_translate("MainWindow", "Выбор файла формата .wav по которому будет создаваться камера"))
        self.pushButton_1.setText(_translate("MainWindow", "Выбрать wav файл"))
        self.pushButton_2.setToolTip(_translate("MainWindow", "Выбор папки с шаблонами из которых будет создаваться камера"))
        self.pushButton_2.setText(_translate("MainWindow", "Выбрать шаблоны камеры"))
        self.label_1.setText(_translate("MainWindow", "Коэффициент свёртки:"))
        self.doubleSpinBox_1.setToolTip(_translate("MainWindow", "Коэффицент свертки массива сэмплов wav-файла, влияет на количество переходов в создаваемой камере"))
        self.label_2.setText(_translate("MainWindow", "Коэффициент поиска переходов:"))
        self.doubleSpinBox_2.setToolTip(_translate("MainWindow", "Коэффициент поиска переходов камеры по сэмплам wav-файла, влияет на позиции переходов в создаваемой камере"))
        self.pushButton_3.setToolTip(_translate("MainWindow", "Создает камеру по wav-файлу из выбранных шаблонов и сохраняет в заданный .vmd файл"))
        self.pushButton_3.setText(_translate("MainWindow", "Создать камеру"))

