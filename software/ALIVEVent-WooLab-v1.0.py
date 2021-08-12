from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
import os
import serial
from serial import SerialException
import time
from random import randint
from PyQt5.Qt import QColor, QDate, QTime
from functools import partial
import datetime
from statistics import mean
import csv


class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2629, 1262)

        self.setupSerial()
        self.setupDataAcq()
        self.setupPalette(MainWindow)

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.centralWidget_VL = QtWidgets.QVBoxLayout(
            self.centralWidget)
        self.centralWidget_VL.setObjectName("centralWidget_VL")

        self.setupStats()
        self.setupGraph1()
        self.setupGraph2()
        self.setupGraph3()
        self.setupDataTimer()
        self.setupBreathingTimer()
        self.setupClockRecordingTimer()

        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 2629, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    ### SETUP UI SUBMETHODS ###

    def setupPalette(self, MainWindow):

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,
                         QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(31, 142, 250))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,
                         QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,
                         QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,
                         QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,
                         QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(22, 34, 60))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,
                         QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,
                         QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,
                         QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(31, 142, 250))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,
                         QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,
                         QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,
                         QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,
                         QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(22, 34, 60))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,
                         QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,
                         QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,
                         QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(31, 142, 250))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,
                         QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,
                         QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,
                         QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(22, 34, 60))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,
                         QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(22, 34, 60))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,
                         QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,
                         QtGui.QPalette.PlaceholderText, brush)
        MainWindow.setPalette(palette)

    def setupStats(self):
        self.stat_widget = QtWidgets.QWidget(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stat_widget.sizePolicy().hasHeightForWidth())
        self.stat_widget.setSizePolicy(sizePolicy)
        self.stat_widget.setObjectName("stat_widget")
        self.stat_widget_HL = QtWidgets.QHBoxLayout(self.stat_widget)
        self.stat_widget_HL.setObjectName("stat_widget_HL")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.stat_widget_HL.addItem(spacerItem)
        
        # self.stat_window = QtWidgets.QWidget(self.stat_widget)
        # self.stat_window.setStyleSheet("background-color: rgb(33, 43, 68);\n"
        #                                "color: rgb(255, 255, 255);\n"
        #                                "border-radius: 16px;")
        # self.stat_window.setObjectName("stat_window")
        # self.stat_window_HL = QtWidgets.QHBoxLayout(self.stat_window)
        # self.stat_window_HL.setObjectName("stat_window_HL")
        
        self.stat_window = QtWidgets.QWidget(self.stat_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stat_window.sizePolicy().hasHeightForWidth())
        self.stat_window.setSizePolicy(sizePolicy)
        self.stat_window.setMinimumSize(QtCore.QSize(1200, 0))
        self.stat_window.setMaximumSize(QtCore.QSize(1200, 16777215))
        self.stat_window.setStyleSheet("background-color: rgb(33, 43, 68);\n"
                                       "color: rgb(255, 255, 255);\n"
                                       "border-radius: 16px;")
        self.stat_window.setObjectName("stat_window")
        self.stat_window_HL = QtWidgets.QHBoxLayout(self.stat_window)
        self.stat_window_HL.setObjectName("stat_window_HL")
        spacerItem1 = QtWidgets.QSpacerItem(
            16, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.stat_window_HL.addItem(spacerItem1)
        
        self.stat_col0 = QtWidgets.QWidget(self.stat_window)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stat_col0.sizePolicy().hasHeightForWidth())
        self.stat_col0.setSizePolicy(sizePolicy)
        self.stat_col0.setObjectName("stat_col0")
        self.stat_col0_VL = QtWidgets.QVBoxLayout(self.stat_col0)
        self.stat_col0_VL.setObjectName("stat_col0_VL")
        self.ITV_value = QtWidgets.QLabel(self.stat_col0)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ITV_value.sizePolicy().hasHeightForWidth())
        self.ITV_value.setSizePolicy(sizePolicy)
        self.ITV_value.setMaximumSize(QtCore.QSize(16777215, 75))
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(60)
        font.setBold(True)
        font.setWeight(75)
        self.ITV_value.setFont(font)
        self.ITV_value.setAlignment(QtCore.Qt.AlignCenter)
        self.ITV_value.setObjectName("ITV_value")
        self.stat_col0_VL.addWidget(self.ITV_value)
        self.ITV_label = QtWidgets.QLabel(self.stat_col0)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ITV_label.sizePolicy().hasHeightForWidth())
        self.ITV_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.ITV_label.setFont(font)
        self.ITV_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ITV_label.setObjectName("ITV_label")
        self.stat_col0_VL.addWidget(self.ITV_label)
        self.stat_col0_sub = QtWidgets.QWidget(self.stat_col0)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stat_col0_sub.sizePolicy().hasHeightForWidth())
        self.stat_col0_sub.setSizePolicy(sizePolicy)
        self.stat_col0_sub.setObjectName("stat_col0_sub")
        self.stat_col0_sub_GL = QtWidgets.QGridLayout(self.stat_col0_sub)
        self.stat_col0_sub_GL.setObjectName("stat_col0_sub_GL")
        self.E2I_button_pos = QtWidgets.QPushButton(self.stat_col0_sub)
        self.E2I_button_pos.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.E2I_button_pos.sizePolicy().hasHeightForWidth())
        self.E2I_button_pos.setSizePolicy(sizePolicy)
        self.E2I_button_pos.setMinimumSize(QtCore.QSize(40, 40))
        self.E2I_button_pos.setMaximumSize(QtCore.QSize(40, 40))
        self.E2I_button_pos.setStyleSheet("background-color: rgb(31, 142, 250);\n"
                                          "font: 18pt \"MS Shell Dlg 2\";\n"
                                          "color: rgb(255, 255, 255);\n"
                                          "border-radius: 8px;\n"
                                          "")
        self.E2I_button_pos.setObjectName("E2I_button_pos")
        self.E2I_button_pos.clicked.connect(
            partial(self.E2I_button_clicked, True))

        self.stat_col0_sub_GL.addWidget(self.E2I_button_pos, 0, 2, 1, 1)
        self.E2I_label = QtWidgets.QLabel(self.stat_col0_sub)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.E2I_label.sizePolicy().hasHeightForWidth())
        self.E2I_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.E2I_label.setFont(font)
        self.E2I_label.setAlignment(QtCore.Qt.AlignCenter)
        self.E2I_label.setObjectName("E2I_label")
        self.stat_col0_sub_GL.addWidget(self.E2I_label, 1, 0, 1, 3)
        self.E2I_value = QtWidgets.QLabel(self.stat_col0_sub)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.E2I_value.sizePolicy().hasHeightForWidth())
        self.E2I_value.setSizePolicy(sizePolicy)
        self.E2I_value.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.E2I_value.setFont(font)
        self.E2I_value.setAlignment(QtCore.Qt.AlignCenter)
        self.E2I_value.setObjectName("E2I_value")
        self.stat_col0_sub_GL.addWidget(self.E2I_value, 0, 1, 1, 1)
        self.E2I_button_neg = QtWidgets.QPushButton(self.stat_col0_sub)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.E2I_button_neg.sizePolicy().hasHeightForWidth())
        self.E2I_button_neg.setSizePolicy(sizePolicy)
        self.E2I_button_neg.setMinimumSize(QtCore.QSize(40, 40))
        self.E2I_button_neg.setMaximumSize(QtCore.QSize(40, 40))
        self.E2I_button_neg.setStyleSheet("background-color: rgb(31, 142, 250);\n"
                                          "font: 18pt \"MS Shell Dlg 2\";\n"
                                          "color: rgb(255, 255, 255);\n"
                                          "border-radius: 8px;")
        self.E2I_button_neg.setObjectName("E2I_button_neg")
        self.E2I_button_neg.clicked.connect(
            partial(self.E2I_button_clicked, False))
        self.stat_col0_sub_GL.addWidget(self.E2I_button_neg, 0, 0, 1, 1)
        self.stat_col0_VL.addWidget(self.stat_col0_sub)
        self.stat_window_HL.addWidget(self.stat_col0)
        spacerItem2 = QtWidgets.QSpacerItem(
            12, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.stat_window_HL.addItem(spacerItem2)
        self.stat_col1 = QtWidgets.QWidget(self.stat_window)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stat_col1.sizePolicy().hasHeightForWidth())
        self.stat_col1.setSizePolicy(sizePolicy)
        self.stat_col1.setObjectName("stat_col1")
        self.stat_col1_VL = QtWidgets.QVBoxLayout(self.stat_col1)
        self.stat_col1_VL.setObjectName("stat_col1_VL")
        self.ETV_value = QtWidgets.QLabel(self.stat_col1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ETV_value.sizePolicy().hasHeightForWidth())
        self.ETV_value.setSizePolicy(sizePolicy)
        self.ETV_value.setMaximumSize(QtCore.QSize(16777215, 75))
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(60)
        font.setBold(True)
        font.setWeight(75)
        self.ETV_value.setFont(font)
        self.ETV_value.setAlignment(QtCore.Qt.AlignCenter)
        self.ETV_value.setObjectName("ETV_value")
        self.stat_col1_VL.addWidget(self.ETV_value)
        self.ETV_label = QtWidgets.QLabel(self.stat_col1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ETV_label.sizePolicy().hasHeightForWidth())
        self.ETV_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.ETV_label.setFont(font)
        self.ETV_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ETV_label.setObjectName("ETV_label")
        self.stat_col1_VL.addWidget(self.ETV_label)
        self.stat_col1_sub = QtWidgets.QWidget(self.stat_col1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stat_col1_sub.sizePolicy().hasHeightForWidth())
        self.stat_col1_sub.setSizePolicy(sizePolicy)
        self.stat_col1_sub.setObjectName("stat_col1_sub")
        self.stat_col1_sub_GL = QtWidgets.QGridLayout(self.stat_col1_sub)
        self.stat_col1_sub_GL.setObjectName("stat_col1_sub_GL")
        self.RR_value = QtWidgets.QLabel(self.stat_col1_sub)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.RR_value.sizePolicy().hasHeightForWidth())
        self.RR_value.setSizePolicy(sizePolicy)
        self.RR_value.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.RR_value.setFont(font)
        self.RR_value.setAlignment(QtCore.Qt.AlignCenter)
        self.RR_value.setObjectName("RR_value")
        self.stat_col1_sub_GL.addWidget(self.RR_value, 0, 1, 1, 1)
        self.RR_button_neg = QtWidgets.QPushButton(self.stat_col1_sub)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.RR_button_neg.sizePolicy().hasHeightForWidth())
        self.RR_button_neg.setSizePolicy(sizePolicy)
        self.RR_button_neg.setMinimumSize(QtCore.QSize(40, 40))
        self.RR_button_neg.setMaximumSize(QtCore.QSize(40, 40))
        self.RR_button_neg.setStyleSheet("background-color: rgb(31, 142, 250);\n"
                                         "font: 18pt \"MS Shell Dlg 2\";\n"
                                         "color: rgb(255, 255, 255);\n"
                                         "border-radius: 8px;")
        self.RR_button_neg.setObjectName("RR_button_neg")
        self.RR_button_neg.clicked.connect(
            partial(self.RR_button_clicked, False))
        self.stat_col1_sub_GL.addWidget(self.RR_button_neg, 0, 0, 1, 1)
        self.RR_button_pos = QtWidgets.QPushButton(self.stat_col1_sub)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.RR_button_pos.sizePolicy().hasHeightForWidth())
        self.RR_button_pos.setSizePolicy(sizePolicy)
        self.RR_button_pos.setMinimumSize(QtCore.QSize(40, 40))
        self.RR_button_pos.setMaximumSize(QtCore.QSize(40, 40))
        self.RR_button_pos.setStyleSheet("background-color: rgb(31, 142, 250);\n"
                                         "font: 18pt \"MS Shell Dlg 2\";\n"
                                         "color: rgb(255, 255, 255);\n"
                                         "border-radius: 8px;")
        self.RR_button_pos.setObjectName("RR_button_pos")
        self.RR_button_pos.clicked.connect(
            partial(self.RR_button_clicked, True))
        self.stat_col1_sub_GL.addWidget(self.RR_button_pos, 0, 2, 1, 1)
        self.RR_label = QtWidgets.QLabel(self.stat_col1_sub)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.RR_label.sizePolicy().hasHeightForWidth())
        self.RR_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.RR_label.setFont(font)
        self.RR_label.setAlignment(QtCore.Qt.AlignCenter)
        self.RR_label.setObjectName("RR_label")
        self.stat_col1_sub_GL.addWidget(self.RR_label, 1, 0, 1, 3)
        self.stat_col1_VL.addWidget(self.stat_col1_sub)
        self.stat_window_HL.addWidget(self.stat_col1)
        spacerItem3 = QtWidgets.QSpacerItem(
            12, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.stat_window_HL.addItem(spacerItem3)
        self.stat_col2 = QtWidgets.QWidget(self.stat_window)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stat_col2.sizePolicy().hasHeightForWidth())
        self.stat_col2.setSizePolicy(sizePolicy)
        self.stat_col2.setObjectName("stat_col2")
        self.stat_col2_VL = QtWidgets.QVBoxLayout(self.stat_col2)
        self.stat_col2_VL.setObjectName("stat_col2_VL")
        self.PEEP_value = QtWidgets.QLabel(self.stat_col2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.PEEP_value.sizePolicy().hasHeightForWidth())
        self.PEEP_value.setSizePolicy(sizePolicy)
        self.PEEP_value.setMaximumSize(QtCore.QSize(16777215, 75))
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(60)
        font.setBold(True)
        font.setWeight(75)
        self.PEEP_value.setFont(font)
        self.PEEP_value.setAlignment(QtCore.Qt.AlignCenter)
        self.PEEP_value.setObjectName("PEEP_value")
        self.stat_col2_VL.addWidget(self.PEEP_value)
        self.PEEP_label = QtWidgets.QLabel(self.stat_col2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.PEEP_label.sizePolicy().hasHeightForWidth())
        self.PEEP_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PEEP_label.setFont(font)
        self.PEEP_label.setAlignment(QtCore.Qt.AlignCenter)
        self.PEEP_label.setObjectName("PEEP_label")
        self.stat_col2_VL.addWidget(self.PEEP_label)
        self.stat_col2_sub = QtWidgets.QWidget(self.stat_col2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stat_col2_sub.sizePolicy().hasHeightForWidth())
        self.stat_col2_sub.setSizePolicy(sizePolicy)
        self.stat_col2_sub.setObjectName("stat_col2_sub")
        self.stat_col1_sub_GL_2 = QtWidgets.QGridLayout(self.stat_col2_sub)
        self.stat_col1_sub_GL_2.setObjectName("stat_col1_sub_GL_2")
        self.sPEEP_value = QtWidgets.QLabel(self.stat_col2_sub)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sPEEP_value.sizePolicy().hasHeightForWidth())
        self.sPEEP_value.setSizePolicy(sizePolicy)
        self.sPEEP_value.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.sPEEP_value.setFont(font)
        self.sPEEP_value.setAlignment(QtCore.Qt.AlignCenter)
        self.sPEEP_value.setObjectName("sPEEP_value")
        self.stat_col1_sub_GL_2.addWidget(self.sPEEP_value, 0, 1, 1, 1)
        self.sPEEP_button_neg = QtWidgets.QPushButton(self.stat_col2_sub)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sPEEP_button_neg.sizePolicy().hasHeightForWidth())
        self.sPEEP_button_neg.setSizePolicy(sizePolicy)
        self.sPEEP_button_neg.setMinimumSize(QtCore.QSize(40, 40))
        self.sPEEP_button_neg.setMaximumSize(QtCore.QSize(40, 40))
        self.sPEEP_button_neg.setStyleSheet("background-color: rgb(31, 142, 250);\n"
                                            "font: 18pt \"MS Shell Dlg 2\";\n"
                                            "color: rgb(255, 255, 255);\n"
                                            "border-radius: 8px;")
        self.sPEEP_button_neg.setObjectName("sPEEP_button_neg")
        self.sPEEP_button_neg.clicked.connect(
            partial(self.sPEEP_button_clicked, False))
        self.stat_col1_sub_GL_2.addWidget(self.sPEEP_button_neg, 0, 0, 1, 1)
        self.sPEEP_button_pos = QtWidgets.QPushButton(self.stat_col2_sub)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sPEEP_button_pos.sizePolicy().hasHeightForWidth())
        self.sPEEP_button_pos.setSizePolicy(sizePolicy)
        self.sPEEP_button_pos.setMinimumSize(QtCore.QSize(40, 40))
        self.sPEEP_button_pos.setMaximumSize(QtCore.QSize(40, 40))
        self.sPEEP_button_pos.setStyleSheet("background-color: rgb(31, 142, 250);\n"
                                            "font: 18pt \"MS Shell Dlg 2\";\n"
                                            "color: rgb(255, 255, 255);\n"
                                            "border-radius: 8px;")
        self.sPEEP_button_pos.setObjectName("sPEEP_button_pos")
        self.sPEEP_button_pos.clicked.connect(
            partial(self.sPEEP_button_clicked, True))
        self.stat_col1_sub_GL_2.addWidget(self.sPEEP_button_pos, 0, 2, 1, 1)
        self.sPEEP_label = QtWidgets.QLabel(self.stat_col2_sub)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sPEEP_label.sizePolicy().hasHeightForWidth())
        self.sPEEP_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.sPEEP_label.setFont(font)
        self.sPEEP_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sPEEP_label.setObjectName("sPEEP_label")
        self.stat_col1_sub_GL_2.addWidget(self.sPEEP_label, 1, 0, 1, 3)
        self.stat_col2_VL.addWidget(self.stat_col2_sub)
        self.stat_window_HL.addWidget(self.stat_col2)
        spacerItem4 = QtWidgets.QSpacerItem(
            16, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.stat_window_HL.addItem(spacerItem4)
        self.stat_col3 = QtWidgets.QWidget(self.stat_window)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stat_col3.sizePolicy().hasHeightForWidth())
        self.stat_col3.setSizePolicy(sizePolicy)
        self.stat_col3.setObjectName("stat_col3")
        self.stat_col3_VL = QtWidgets.QVBoxLayout(self.stat_col3)
        self.stat_col3_VL.setObjectName("stat_col3_VL")
        self.PIP_value = QtWidgets.QLabel(self.stat_col3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.PIP_value.sizePolicy().hasHeightForWidth())
        self.PIP_value.setSizePolicy(sizePolicy)
        self.PIP_value.setMaximumSize(QtCore.QSize(16777215, 75))
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(60)
        font.setBold(True)
        font.setWeight(75)
        self.PIP_value.setFont(font)
        self.PIP_value.setAlignment(QtCore.Qt.AlignCenter)
        self.PIP_value.setObjectName("PIP_value")
        self.stat_col3_VL.addWidget(self.PIP_value)
        self.PIP_label = QtWidgets.QLabel(self.stat_col3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.PIP_label.sizePolicy().hasHeightForWidth())
        self.PIP_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PIP_label.setFont(font)
        self.PIP_label.setAlignment(QtCore.Qt.AlignCenter)
        self.PIP_label.setObjectName("PIP_label")
        self.stat_col3_VL.addWidget(self.PIP_label)
        self.stat_col3_sub = QtWidgets.QWidget(self.stat_col3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stat_col3_sub.sizePolicy().hasHeightForWidth())
        self.stat_col3_sub.setSizePolicy(sizePolicy)
        self.stat_col3_sub.setObjectName("stat_col3_sub")
        self.stat_col1_sub_GL_3 = QtWidgets.QGridLayout(self.stat_col3_sub)
        self.stat_col1_sub_GL_3.setObjectName("stat_col1_sub_GL_3")
        self.sPIP_value = QtWidgets.QLabel(self.stat_col3_sub)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sPIP_value.sizePolicy().hasHeightForWidth())
        self.sPIP_value.setSizePolicy(sizePolicy)
        self.sPIP_value.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.sPIP_value.setFont(font)
        self.sPIP_value.setAlignment(QtCore.Qt.AlignCenter)
        self.sPIP_value.setObjectName("sPIP_value")
        self.stat_col1_sub_GL_3.addWidget(self.sPIP_value, 0, 1, 1, 1)
        self.sPIP_button_neg = QtWidgets.QPushButton(self.stat_col3_sub)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sPIP_button_neg.sizePolicy().hasHeightForWidth())
        self.sPIP_button_neg.setSizePolicy(sizePolicy)
        self.sPIP_button_neg.setMinimumSize(QtCore.QSize(40, 40))
        self.sPIP_button_neg.setMaximumSize(QtCore.QSize(40, 40))
        self.sPIP_button_neg.setStyleSheet("background-color: rgb(31, 142, 250);\n"
                                           "font: 18pt \"MS Shell Dlg 2\";\n"
                                           "color: rgb(255, 255, 255);\n"
                                           "border-radius: 8px;")
        self.sPIP_button_neg.setObjectName("sPIP_button_neg")
        self.sPIP_button_neg.clicked.connect(
            partial(self.sPIP_button_clicked, False))
        self.stat_col1_sub_GL_3.addWidget(self.sPIP_button_neg, 0, 0, 1, 1)
        self.sPIP_button_pos = QtWidgets.QPushButton(self.stat_col3_sub)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sPIP_button_pos.sizePolicy().hasHeightForWidth())
        self.sPIP_button_pos.setSizePolicy(sizePolicy)
        self.sPIP_button_pos.setMinimumSize(QtCore.QSize(40, 40))
        self.sPIP_button_pos.setMaximumSize(QtCore.QSize(40, 40))
        self.sPIP_button_pos.setStyleSheet("background-color: rgb(31, 142, 250);\n"
                                           "font: 18pt \"MS Shell Dlg 2\";\n"
                                           "color: rgb(255, 255, 255);\n"
                                           "border-radius: 8px;")
        self.sPIP_button_pos.setObjectName("sPIP_button_pos")
        self.sPIP_button_pos.clicked.connect(
            partial(self.sPIP_button_clicked, True))
        self.stat_col1_sub_GL_3.addWidget(self.sPIP_button_pos, 0, 2, 1, 1)
        self.sPIP_label = QtWidgets.QLabel(self.stat_col3_sub)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sPIP_label.sizePolicy().hasHeightForWidth())
        self.sPIP_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.sPIP_label.setFont(font)
        self.sPIP_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sPIP_label.setObjectName("sPIP_label")
        self.stat_col1_sub_GL_3.addWidget(self.sPIP_label, 1, 0, 1, 3)
        self.stat_col3_VL.addWidget(self.stat_col3_sub)
        self.stat_window_HL.addWidget(self.stat_col3)
        spacerItem5 = QtWidgets.QSpacerItem(
            16, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.stat_window_HL.addItem(spacerItem5)
        self.stat_col4 = QtWidgets.QWidget(self.stat_window)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stat_col4.sizePolicy().hasHeightForWidth())
        self.stat_col4.setSizePolicy(sizePolicy)
        self.stat_col4.setObjectName("stat_col4")
        self.stat_col2_VL_2 = QtWidgets.QVBoxLayout(self.stat_col4)
        self.stat_col2_VL_2.setObjectName("stat_col2_VL_2")
        self.O2_value = QtWidgets.QLabel(self.stat_col4)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.O2_value.sizePolicy().hasHeightForWidth())
        self.O2_value.setSizePolicy(sizePolicy)
        self.O2_value.setMaximumSize(QtCore.QSize(16777215, 75))
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(60)
        font.setBold(True)
        font.setWeight(75)
        self.O2_value.setFont(font)
        self.O2_value.setAlignment(QtCore.Qt.AlignCenter)
        self.O2_value.setObjectName("O2_value")
        self.stat_col2_VL_2.addWidget(self.O2_value)
        self.O2_label = QtWidgets.QLabel(self.stat_col4)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.O2_label.sizePolicy().hasHeightForWidth())
        self.O2_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.O2_label.setFont(font)
        self.O2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.O2_label.setObjectName("O2_label")
        self.stat_col2_VL_2.addWidget(self.O2_label)
        self.stat_col3_sub_3 = QtWidgets.QWidget(self.stat_col4)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stat_col3_sub_3.sizePolicy().hasHeightForWidth())
        self.stat_col3_sub_3.setSizePolicy(sizePolicy)
        self.stat_col3_sub_3.setObjectName("stat_col3_sub_3")
        self.stat_col1_sub_GL_4 = QtWidgets.QGridLayout(self.stat_col3_sub_3)
        self.stat_col1_sub_GL_4.setObjectName("stat_col1_sub_GL_4")
        self.PHASE_value = QtWidgets.QLabel(self.stat_col3_sub_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.PHASE_value.sizePolicy().hasHeightForWidth())
        self.PHASE_value.setSizePolicy(sizePolicy)
        self.PHASE_value.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.PHASE_value.setFont(font)
        self.PHASE_value.setAlignment(QtCore.Qt.AlignCenter)
        self.PHASE_value.setObjectName("PHASE_value")
        self.stat_col1_sub_GL_4.addWidget(self.PHASE_value, 0, 1, 1, 1)
        self.PHASE_label = QtWidgets.QLabel(self.stat_col3_sub_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.PHASE_label.sizePolicy().hasHeightForWidth())
        self.PHASE_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PHASE_label.setFont(font)
        self.PHASE_label.setAlignment(QtCore.Qt.AlignCenter)
        self.PHASE_label.setObjectName("PHASE_label")
        self.stat_col1_sub_GL_4.addWidget(self.PHASE_label, 1, 0, 1, 3)
        self.stat_col2_VL_2.addWidget(self.stat_col3_sub_3)
        self.stat_window_HL.addWidget(self.stat_col4)
        self.stat_widget_HL.addWidget(self.stat_window)
        spacerItem6 = QtWidgets.QSpacerItem(
            16, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.stat_widget_HL.addItem(spacerItem6)
        self.time_widget = QtWidgets.QWidget(self.stat_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.time_widget.sizePolicy().hasHeightForWidth())
        self.time_widget.setSizePolicy(sizePolicy)
        self.time_widget.setMinimumSize(QtCore.QSize(320, 0))
        self.time_widget.setMaximumSize(QtCore.QSize(320, 16777215))
        self.time_widget.setStyleSheet("background-color: rgb(33, 43, 68);\n"
                                       "color: rgb(255, 255, 255);\n"
                                       "border-radius: 16px;\n"
                                       "")
        self.time_widget.setObjectName("time_widget")
        self.time_widget_VL = QtWidgets.QVBoxLayout(self.time_widget)
        self.time_widget_VL.setObjectName("time_widget_VL")
        self.time_value = QtWidgets.QLabel(self.time_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.time_value.sizePolicy().hasHeightForWidth())
        self.time_value.setSizePolicy(sizePolicy)
        self.time_value.setMaximumSize(QtCore.QSize(16777215, 75))
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(44)
        font.setBold(True)
        font.setWeight(75)
        self.time_value.setFont(font)
        self.time_value.setAlignment(QtCore.Qt.AlignCenter)
        self.time_value.setObjectName("time_value")
        self.time_widget_VL.addWidget(self.time_value)
        self.time_label = QtWidgets.QLabel(self.time_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.time_label.sizePolicy().hasHeightForWidth())
        self.time_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.time_label.setFont(font)
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.time_label.setObjectName("time_label")
        self.time_widget_VL.addWidget(self.time_label)
        self.vent_time_widget = QtWidgets.QWidget(self.time_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.vent_time_widget.sizePolicy().hasHeightForWidth())
        self.vent_time_widget.setSizePolicy(sizePolicy)
        self.vent_time_widget.setMaximumSize(QtCore.QSize(16777215, 75))
        self.vent_time_widget.setObjectName("vent_time_widget")
        self.vent_time_widget_HL = QtWidgets.QHBoxLayout(self.vent_time_widget)
        self.vent_time_widget_HL.setObjectName("vent_time_widget_HL")
        self.vent_time_value = QtWidgets.QLabel(self.vent_time_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.vent_time_value.sizePolicy().hasHeightForWidth())
        self.vent_time_value.setSizePolicy(sizePolicy)
        self.vent_time_value.setMinimumSize(QtCore.QSize(0, 0))
        self.vent_time_value.setMaximumSize(QtCore.QSize(16777215, 75))
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(44)
        font.setBold(True)
        font.setWeight(75)
        self.vent_time_value.setFont(font)
        self.vent_time_value.setAlignment(QtCore.Qt.AlignCenter)
        self.vent_time_value.setObjectName("vent_time_value")
        self.vent_time_widget_HL.addWidget(self.vent_time_value)
        self.record_button = QtWidgets.QPushButton(self.vent_time_widget)
        self.record_button.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.record_button.sizePolicy().hasHeightForWidth())
        self.record_button.setSizePolicy(sizePolicy)
        self.record_button.setMinimumSize(QtCore.QSize(50, 50))
        self.record_button.setMaximumSize(QtCore.QSize(40, 40))
        self.record_button.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                                         "font: 18pt \"MS Shell Dlg 2\";\n"
                                         "color: rgb(255, 255, 255);\n"
                                         "border-radius:25px;\n"
                                         "")
        self.record_button.setObjectName("record_button")
        
        self.record_button.clicked.connect(
            partial(self.recordButtonClicked))
            
        self.vent_time_widget_HL.addWidget(self.record_button)
        self.time_widget_VL.addWidget(self.vent_time_widget)
        self.vent_time_label = QtWidgets.QLabel(self.time_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.vent_time_label.sizePolicy().hasHeightForWidth())
        self.vent_time_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.vent_time_label.setFont(font)
        self.vent_time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.vent_time_label.setObjectName("vent_time_label")
        self.time_widget_VL.addWidget(self.vent_time_label)
        self.stat_widget_HL.addWidget(self.time_widget)
        spacerItem7 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.stat_widget_HL.addItem(spacerItem7)
        self.centralWidget_VL.addWidget(self.stat_widget)

    # Graph 1: Inspiratory Flow Rate
    def setupGraph1(self):
        self.graph1_widget = QtWidgets.QWidget(self.centralWidget)
        self.graph1_widget.setObjectName("graph1_widget")
        self.graph1_widget_HL = QtWidgets.QHBoxLayout(
            self.graph1_widget)
        self.graph1_widget_HL.setObjectName("graph1_widget_HL")
        self.graph1_label_widget = QtWidgets.QWidget(
            self.graph1_widget)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.graph1_label_widget.sizePolicy().hasHeightForWidth())
        self.graph1_label_widget.setSizePolicy(sizePolicy)

        self.graph1_label_widget.setStyleSheet("background-color: rgb(33, 43, 68);\n"
                                               "color: rgb(255, 255, 255);\n"
                                               "border-radius: 16px;")
        self.graph1_label_widget.setObjectName("graph1_label_widget")
        self.graph1_label_widget_HL = QtWidgets.QHBoxLayout(
            self.graph1_label_widget)
        self.graph1_label_widget_HL.setObjectName(
            "graph1_label_widget_HL")
        spacerItem8 = QtWidgets.QSpacerItem(
            8, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.graph1_label_widget_HL.addItem(spacerItem8)
        self.graph1_label = QtWidgets.QLabel(self.graph1_label_widget)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.graph1_label.sizePolicy().hasHeightForWidth())
        self.graph1_label.setSizePolicy(sizePolicy)

        self.graph1_label.setMinimumSize(QtCore.QSize(75, 0))
        self.graph1_label.setMaximumSize(QtCore.QSize(75, 16777215))

        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(60)
        self.graph1_label.setFont(font)

        self.graph1_label.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.graph1_label.setObjectName("graph1_label")
        self.graph1_label_widget_HL.addWidget(self.graph1_label)
        self.graph1_value_widget = QtWidgets.QWidget(
            self.graph1_label_widget)
        self.graph1_value_widget.setMinimumSize(QtCore.QSize(100, 0))
        self.graph1_value_widget.setObjectName("graph1_value_widget")
        self.graph1_value_widget_VL = QtWidgets.QVBoxLayout(
            self.graph1_value_widget)
        self.graph1_value_widget_VL.setObjectName(
            "graph1_value_widget_VL")
        self.graph1_value = QtWidgets.QLabel(self.graph1_value_widget)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.graph1_value.sizePolicy().hasHeightForWidth())
        self.graph1_value.setSizePolicy(sizePolicy)
        self.graph1_value.setMinimumSize(QtCore.QSize(200, 0))
        self.graph1_value.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(60)
        font.setBold(True)
        font.setWeight(60)
        self.graph1_value.setFont(font)
        self.graph1_value.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.graph1_value.setObjectName("graph1_value")
        self.graph1_value_widget_VL.addWidget(self.graph1_value)
        self.graph1_units = QtWidgets.QLabel(self.graph1_value_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.graph1_units.sizePolicy().hasHeightForWidth())
        self.graph1_units.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.graph1_units.setFont(font)
        self.graph1_units.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.graph1_units.setObjectName("graph1_units")
        self.graph1_value_widget_VL.addWidget(self.graph1_units)
        self.graph1_label_widget_HL.addWidget(self.graph1_value_widget)
        spacerItem9 = QtWidgets.QSpacerItem(
            8, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.graph1_label_widget_HL.addItem(spacerItem9)
        self.graph1_widget_HL.addWidget(self.graph1_label_widget)
        spacerItem10 = QtWidgets.QSpacerItem(
            16, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.graph1_widget_HL.addItem(spacerItem10)
        self.graph1_window = QtWidgets.QWidget(self.graph1_widget)
        self.graph1_window.setStyleSheet("background-color: rgb(33, 43, 68);\n"
                                         "color: rgb(255, 255, 255);\n"
                                         "border-radius: 16px;")
        self.graph1_window.setObjectName("graph1_window")
        self.graph1_window_HL = QtWidgets.QHBoxLayout(
            self.graph1_window)
        self.graph1_window_HL.setObjectName("graph1_window_HL")

        self.graph1 = pg.PlotWidget()
        self.graph1.setObjectName("graph1")
        self.graph1_x = [0] 
        self.graph1_y = [0]
        self.graph1.setBackground((0, 0, 0, 0))
        pen = pg.mkPen(color=(5, 201, 133), width=3)
        self.graph1_data_line = self.graph1.plot(
            self.graph1_x, self.graph1_y, pen=pen)

        self.graph1_window_HL.addWidget(self.graph1)
        self.graph1_widget_HL.addWidget(self.graph1_window)
        self.centralWidget_VL.addWidget(self.graph1_widget)

    # Graph 2: Expiratory Flow Rate
    def setupGraph2(self):
        self.graph2_widget = QtWidgets.QWidget(self.centralWidget)
        self.graph2_widget.setObjectName("graph2_widget")
        self.graph2_widget_HL = QtWidgets.QHBoxLayout(
            self.graph2_widget)
        self.graph2_widget_HL.setObjectName("graph2_widget_HL")
        self.graph2_label_widget = QtWidgets.QWidget(
            self.graph2_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.graph2_label_widget.sizePolicy().hasHeightForWidth())
        self.graph2_label_widget.setSizePolicy(sizePolicy)
        self.graph2_label_widget.setStyleSheet("background-color: rgb(33, 43, 68);\n"
                                               "color: rgb(255, 255, 255);\n"
                                               "border-radius: 16px;")
        self.graph2_label_widget.setObjectName("graph2_label_widget")
        self.graph2_label_widget_HL = QtWidgets.QHBoxLayout(
            self.graph2_label_widget)
        self.graph2_label_widget_HL.setObjectName(
            "graph2_label_widget_HL")
        spacerItem11 = QtWidgets.QSpacerItem(
            8, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.graph2_label_widget_HL.addItem(spacerItem11)
        self.graph2_label = QtWidgets.QLabel(self.graph2_label_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.graph2_label.sizePolicy().hasHeightForWidth())
        self.graph2_label.setSizePolicy(sizePolicy)
        self.graph2_label.setMinimumSize(QtCore.QSize(75, 0))
        self.graph2_label.setMaximumSize(QtCore.QSize(75, 16777215))
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(60)
        self.graph2_label.setFont(font)
        self.graph2_label.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.graph2_label.setObjectName("graph2_label")
        self.graph2_label_widget_HL.addWidget(self.graph2_label)
        self.graph2_value_widget = QtWidgets.QWidget(
            self.graph2_label_widget)
        self.graph2_value_widget.setMinimumSize(QtCore.QSize(100, 0))
        self.graph2_value_widget.setObjectName("graph2_value_widget")
        self.graph2_value_widget_VL = QtWidgets.QVBoxLayout(
            self.graph2_value_widget)
        self.graph2_value_widget_VL.setObjectName(
            "graph2_value_widget_VL")
        self.graph2_value = QtWidgets.QLabel(self.graph2_value_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.graph2_value.sizePolicy().hasHeightForWidth())
        self.graph2_value.setSizePolicy(sizePolicy)
        self.graph2_value.setMinimumSize(QtCore.QSize(200, 0))
        self.graph2_value.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(60)
        font.setBold(True)
        font.setWeight(60)
        self.graph2_value.setFont(font)
        self.graph2_value.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.graph2_value.setObjectName("graph2_value")
        self.graph2_value_widget_VL.addWidget(self.graph2_value)
        self.graph2_units = QtWidgets.QLabel(self.graph2_value_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.graph2_units.sizePolicy().hasHeightForWidth())
        self.graph2_units.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.graph2_units.setFont(font)
        self.graph2_units.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.graph2_units.setObjectName("graph2_units")
        self.graph2_value_widget_VL.addWidget(self.graph2_units)
        self.graph2_label_widget_HL.addWidget(self.graph2_value_widget)
        spacerItem12 = QtWidgets.QSpacerItem(
            8, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.graph2_label_widget_HL.addItem(spacerItem12)
        self.graph2_widget_HL.addWidget(self.graph2_label_widget)
        spacerItem13 = QtWidgets.QSpacerItem(
            16, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.graph2_widget_HL.addItem(spacerItem13)
        self.graph2_window = QtWidgets.QWidget(self.graph2_widget)
        self.graph2_window.setStyleSheet("background-color: rgb(33, 43, 68);\n"
                                         "color: rgb(255, 255, 255);\n"
                                         "border-radius: 16px;\n"
                                         "")
        self.graph2_window.setObjectName("graph2_window")
        self.graph2_window_HL = QtWidgets.QHBoxLayout(
            self.graph2_window)
        self.graph2_window_HL.setObjectName("graph2_window_HL")

        self.graph2 = pg.PlotWidget()
        self.graph2.setObjectName("graph2")
        self.graph2_x = [0]  # 100 time points
        self.graph2_y = [0]  # 100 data points
        self.graph2.setBackground((0, 0, 0, 0))
        pen = pg.mkPen(color=(214, 106, 199), width=3)
        self.graph2_data_line = self.graph2.plot(
            self.graph2_x, self.graph2_y, pen=pen)

        self.graph2_window_HL.addWidget(self.graph2)
        self.graph2_widget_HL.addWidget(self.graph2_window)
        self.centralWidget_VL.addWidget(self.graph2_widget)

    # Graph 3: Lung Pressure
    def setupGraph3(self):
        self.graph3_widget = QtWidgets.QWidget(self.centralWidget)
        self.graph3_widget.setObjectName("graph3_widget")
        self.graph3_widget_HL = QtWidgets.QHBoxLayout(
            self.graph3_widget)
        self.graph3_widget_HL.setObjectName("graph3_widget_HL")
        self.graph3_label_widget = QtWidgets.QWidget(
            self.graph3_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.graph3_label_widget.sizePolicy().hasHeightForWidth())
        self.graph3_label_widget.setSizePolicy(sizePolicy)
        self.graph3_label_widget.setStyleSheet("background-color: rgb(33, 43, 68);\n"
                                               "color: rgb(255, 255, 255);\n"
                                               "border-radius: 16px;")
        self.graph3_label_widget.setObjectName("graph3_label_widget")
        self.graph3_label_widget_HL = QtWidgets.QHBoxLayout(
            self.graph3_label_widget)
        self.graph3_label_widget_HL.setObjectName(
            "graph3_label_widget_HL")
        spacerItem14 = QtWidgets.QSpacerItem(
            8, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.graph3_label_widget_HL.addItem(spacerItem14)
        self.graph3_label = QtWidgets.QLabel(self.graph3_label_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.graph3_label.sizePolicy().hasHeightForWidth())
        self.graph3_label.setSizePolicy(sizePolicy)
        self.graph3_label.setMinimumSize(QtCore.QSize(75, 0))
        self.graph3_label.setMaximumSize(QtCore.QSize(75, 16777215))
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(60)
        self.graph3_label.setFont(font)
        self.graph3_label.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.graph3_label.setObjectName("graph3_label")
        self.graph3_label_widget_HL.addWidget(self.graph3_label)
        self.graph3_value_widget = QtWidgets.QWidget(
            self.graph3_label_widget)
        self.graph3_value_widget.setMinimumSize(QtCore.QSize(100, 0))
        self.graph3_value_widget.setObjectName("graph3_value_widget")
        self.graph3_value_widget_VL = QtWidgets.QVBoxLayout(
            self.graph3_value_widget)
        self.graph3_value_widget_VL.setObjectName(
            "graph3_value_widget_VL")
        self.graph3_value = QtWidgets.QLabel(self.graph3_value_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.graph3_value.sizePolicy().hasHeightForWidth())
        self.graph3_value.setSizePolicy(sizePolicy)
        self.graph3_value.setMinimumSize(QtCore.QSize(200, 0))
        self.graph3_value.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(60)
        font.setBold(True)
        font.setWeight(60)
        self.graph3_value.setFont(font)
        self.graph3_value.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.graph3_value.setObjectName("graph3_value")
        self.graph3_value_widget_VL.addWidget(self.graph3_value)
        self.graph3_units = QtWidgets.QLabel(self.graph3_value_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.graph3_units.sizePolicy().hasHeightForWidth())
        self.graph3_units.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.graph3_units.setFont(font)
        self.graph3_units.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.graph3_units.setObjectName("graph3_units")
        self.graph3_value_widget_VL.addWidget(self.graph3_units)
        self.graph3_label_widget_HL.addWidget(self.graph3_value_widget)
        spacerItem15 = QtWidgets.QSpacerItem(
            8, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.graph3_label_widget_HL.addItem(spacerItem15)
        self.graph3_widget_HL.addWidget(self.graph3_label_widget)
        spacerItem16 = QtWidgets.QSpacerItem(
            16, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.graph3_widget_HL.addItem(spacerItem16)
        self.graph3_window = QtWidgets.QWidget(self.graph3_widget)
        self.graph3_window.setStyleSheet("background-color: rgb(33, 43, 68);\n"
                                         "color: rgb(255, 255, 255);\n"
                                         "border-radius: 16px;")
        self.graph3_window.setObjectName("graph3_window")
        self.graph3_window_HL = QtWidgets.QHBoxLayout(
            self.graph3_window)
        self.graph3_window_HL.setObjectName("graph3_window_HL")

        self.graph3 = pg.PlotWidget()
        self.graph3.setObjectName("graph3")
        self.graph3_x = [0]
        self.graph3_y = [0]
        self.graph3.setBackground((0, 0, 0, 0))
        pen = pg.mkPen(color=(31, 148, 243), width=3)
        self.graph3_data_line = self.graph3.plot(
            self.graph3_x, self.graph3_y, pen=pen)

        self.graph3_window_HL.addWidget(self.graph3)
        self.graph3_widget_HL.addWidget(self.graph3_window)
        self.centralWidget_VL.addWidget(self.graph3_widget)

    ### SETUP DATA ACQUISITON SUBMETHODS ###
    
    def setupSerial(self):
        port1 = "/dev/cu.wchusbserial14140"
        port2 = "/dev/cu.wchusbserial13"

        # port1 = "COM6"
        # port2 = "COM3"
        try:
            self.ser1_sol = serial.Serial(port1, 115200, timeout=1)
            self.ser2 = serial.Serial(port2, 115200, timeout=1)
        except SerialException:
            print("Port not available")

    def setupDataAcq(self):
        self.dataRefreshRate = 100
        self.ITV = 0
        self.ETV = 0
        self.PEEP = 0
        self.PIP = 0

        self.insFlowData_singleCycle = []
        self.expFlowData_singleCycle = []

    ### SETUP TIMER SUBMETHODS ###

    def setupDataTimer(self):
        self.dataRefreshRateTimer = QtCore.QTimer()
        self.dataRefreshRateTimer.setInterval(self.dataRefreshRate)
        self.dataRefreshRateTimer.timeout.connect(self.updateData)
        self.dataRefreshRateTimer.start()

    def setupBreathingTimer(self):
        self.E2I = 2  # Inspiration Time Interval (ratio)
        self.RR = 35  # Expiration Time Interval (rate)
        self.sPEEP = 2 # PEEP
        self.sPIP = 20 # PIP
        self.insPhase = True  # Inspiration Phase Boolean

        self.breathCycleTimer = QtCore.QTimer()
        self.breathCycleTimer.setInterval(100)
        self.breathCycleTimer.timeout.connect(self.updateBreathCycle)
        self.breathCycleTimer.start()

    def setupClockRecordingTimer(self):
        self.isRecording = False
        self.ventTimer_s = 0
        self.ventTimer_data = 0
        self.perfCounter = 0

        self.updateClock()
        self.clockTimer = QtCore.QTimer()
        self.clockTimer.setInterval(1000)
        self.clockTimer.timeout.connect(self.updateClock)
        self.clockTimer.start()

    ### ACTION METHODS ###

    def E2I_button_clicked(self, isPos):
        self.E2I = self.E2I + ((-0.1 if not isPos and self.E2I > 0 else 0.1) * (0 if not isPos and self.E2I <= 0 else 1))
        _translate = QtCore.QCoreApplication.translate
        self.E2I = round((self.E2I),1)
        self.E2I_value.setText(_translate("MainWindow", str(self.E2I)))

    def RR_button_clicked(self, isPos):
        self.RR = self.RR + ((-0.1 if not isPos and self.RR > 0 else 0.1) * (0 if not isPos and self.RR <= 0 else 1))
        _translate = QtCore.QCoreApplication.translate
        self.RR = round((self.RR),1)
        self.RR_value.setText(_translate("MainWindow", str(self.RR)))

    def sPEEP_button_clicked(self, isPos):
        self.sPEEP = self.sPEEP + ((-0.1 if not isPos and self.sPEEP > 0 else 0.1) * (0 if not isPos and self.sPEEP <= 0 else 1))
        _translate = QtCore.QCoreApplication.translate
        self.sPEEP = round((self.sPEEP),1)
        self.sPEEP_value.setText(_translate("MainWindow", str(self.sPEEP)))

    def sPIP_button_clicked(self, isPos):
        self.sPIP = self.sPIP + ((-0.1 if not isPos and self.sPIP > 0 else 0.1) * (0 if not isPos and self.sPIP <= 0 else 1))
        _translate = QtCore.QCoreApplication.translate
        self.sPIP = round((self.sPIP),1)
        self.sPIP_value.setText(_translate("MainWindow", str(self.sPIP)))

    def recordButtonClicked(self):
        _translate = QtCore.QCoreApplication.translate
        self.isRecording = not self.isRecording

        if not self.isRecording:
            self.record_button.setText(_translate("MainWindow", "•"))
        else:
            self.record_button.setText(_translate("MainWindow", "■"))
            date = QDate.currentDate()
            dateValue = date.toString('yyyy-MM-dd')
            time = QTime.currentTime()
            timeValue = time.toString('hh-mm-ss')
            self.csvFilename = "VentilatorRecording_" + dateValue + "_" + timeValue + ".csv"
            
            with open(self.csvFilename, 'w', newline='') as csvfile:
                dataWriter = csv.writer(csvfile)
                dataWriter.writerow(["Time (s)", "Lung Pressure (mmHg)", "Inspiration Flow Rate (SLPM)", "Expiration Flow Rate (SLPM)", "FiO2 (%)"])

    ### UPDATE METHODS ###

    def updateBreathCycle(self):
        _translate = QtCore.QCoreApplication.translate

        # NOTE!!!
        # E2I = E:I Ratio
        # RR = Respiratory Rate

        self.breathCycleTimer.setInterval(
            ((60/self.RR)*(self.E2I/(self.E2I+1))*1000) if self.insPhase else ((60/self.RR)*(1/(self.E2I+1))*1000))
        self.insPhase = not self.insPhase

        if not self.insPhase and self.insFlowData_singleCycle:
            self.ITV = mean(self.insFlowData_singleCycle) * 1000/60 * ((60/self.RR)*(1/(self.E2I+1)))
            print(f'Vt: {round(self.ITV,1)} | Max: {max(self.insFlowData_singleCycle)} | Mean {round(mean(self.insFlowData_singleCycle),1)}')
            
            self.insFlowData_singleCycle.clear()
            self.ITV_value.setText(_translate(
            "MainWindow", str(round(self.ITV))))
        elif self.insPhase and self.expFlowData_singleCycle:
            self.ETV = mean(self.expFlowData_singleCycle) * 1000/60 * ((60/self.RR)*(self.E2I/(self.E2I+1)))
            self.expFlowData_singleCycle.clear()
            self.ETV_value.setText(_translate(
            "MainWindow", str(round(self.ETV))))

        if self.insPhase:
            self.PIP = sys.float_info.min
            try:
                self.ser1_sol.write(b'i')                                 # write to port
            except:
                pass
        else:
            self.PEEP = sys.float_info.max
            try:
                self.ser1_sol.write(b'e')                                 # write to port
            except:
                pass

        self.PHASE_value.setText(_translate(
            "MainWindow", "INS" if self.insPhase else "EXP"))
        self.PHASE_value.setStyleSheet("color: rgb(5, 201, 133);" if self.insPhase else "color: rgb(214, 106, 199);")
        self.PHASE_label.setStyleSheet("color: rgb(5, 201, 133);" if self.insPhase else "color: rgb(214, 106, 199);")

    def updateData(self):
        _translate = QtCore.QCoreApplication.translate
        
        try:
            self.ser1_sol.write(b'g')                                 # write to port
            expFlowPoint = float(self.ser1_sol.readline().decode('Ascii').rstrip("\r\n"))
            O2_value = int(self.ser1_sol.readline().decode('Ascii').rstrip("\r\n"))
        except:
            expFlowPoint = 0
            O2_value = 0

        try:
            self.ser2.write(b'g')                                 # write to port
            insFlowPoint = float(self.ser2.readline().decode('Ascii').rstrip("\r\n"))
            lungPrVal = int(self.ser2.readline().decode('Ascii').rstrip("\r\n"))
        except:
            insFlowPoint = 0 
            lungPrVal = 0

        insFlowPoint = round(insFlowPoint, 1)
        expFlowPoint = round(expFlowPoint, 1)
        lungPrPoint = round(((((lungPrVal/1023) * 5) - 0.5) / 4) * 51.7149, 1)

        elapsedTime = time.perf_counter() - self.perfCounter
        self.perfCounter += elapsedTime

        # FiO2 (%)
        O2_value_str = str(round(((O2_value-204.6)/818.4)*100, 1)) + "%"
        self.O2_value.setText(_translate("MainWindow", O2_value_str))

        # Graph 1: Inspiratory Flow
        if len(self.graph1_x) >= 100:
            self.graph1_x = self.graph1_x[1:]  # Remove the first x element.
            self.graph1_y = self.graph1_y[1:]  # Remove the first y element.
        self.graph1_x.append(self.graph1_x[-1] + elapsedTime)  # Add a new value 1 higher than the last.
        # insFlowPoint = randint(0, 100)  # Read Ins Flow Sensor
        self.graph1_y.append(insFlowPoint)  # Add the new value
        self.graph1_data_line.setData(self.graph1_x, self.graph1_y)  # Update the data.
        self.graph1_value.setText(_translate("MainWindow", str(insFlowPoint)))  # Update graph1 value label
        if self.insPhase:
            self.insFlowData_singleCycle.append(insFlowPoint)

        # Graph 2: Expiratory Flow
        if len(self.graph2_x) >= 100:
            self.graph2_x = self.graph2_x[1:]  # Remove the first x element.
            self.graph2_y = self.graph2_y[1:]  # Remove the first y element.
        self.graph2_x.append(self.graph2_x[-1] + elapsedTime)
        # expFlowPoint = randint(0, 100)  # Read Exp Flow Sensor
        self.graph2_y.append(expFlowPoint)  # Add a new random value
        self.graph2_data_line.setData(self.graph2_x, self.graph2_y)  # Update the data.
        self.graph2_value.setText(_translate("MainWindow", str(expFlowPoint)))  # Update graph2 value label
        if not self.insPhase:
            self.expFlowData_singleCycle.append(expFlowPoint)

        # Graph 3: Lung Pressure
        if len(self.graph3_x) >= 100:
            
            self.graph3_x = self.graph3_x[1:]  # Remove the first x element.
            self.graph3_y = self.graph3_y[1:]  # Remove the first y element.
        self.graph3_x.append(self.graph3_x[-1] + elapsedTime)  # Add a new value 1 higher than the last.
        # lungPrPoint = randint(0, 20)  # Read pressure sensor
        self.graph3_y.append(lungPrPoint)  # Add a new random value
        self.graph3_data_line.setData(self.graph3_x, self.graph3_y)  # Update the data.
        self.graph3_value.setText(_translate("MainWindow", str(lungPrPoint)))  # Update graph3 value label
        
        # PEEP/PIP (mmHg)
        if self.insPhase and lungPrPoint > self.PIP:
            self.PIP = lungPrPoint
            self.PIP_value.setText(_translate(
                "MainWindow", str(round(self.PIP))))  # Update value label
            # SAFETY LOGIC
            if self.PIP >= self.sPIP:    
                try:
                    self.ser1_sol.write(b's')                                 # write to port
                except:
                    pass
        elif not self.insPhase and lungPrPoint < self.PEEP:
            self.PEEP = lungPrPoint
            self.PEEP_value.setText(_translate(
                "MainWindow", str(round(self.PEEP))))  # Update value label
            # SAFETY LOGIC
            if self.PEEP <= self.sPEEP:    
                try:
                    self.ser1_sol.write(b's')                                 # write to port
                except:
                    pass

        
        # Write to file
        if self.isRecording:
            self.ventTimer_data += elapsedTime
            with open(self.csvFilename, 'a', newline='') as csvfile:
                dataWriter = csv.writer(csvfile)
                dataWriter.writerow([self.ventTimer_data, lungPrPoint, insFlowPoint,expFlowPoint, O2_value])

    def updateClock(self):
        _translate = QtCore.QCoreApplication.translate

        time = QTime.currentTime()
        timeValue = time.toString('hh:mm:ss')

        if self.isRecording:
            self.ventTimer_s += 1
            ventTimeValue = datetime.timedelta(seconds=self.ventTimer_s)
            self.vent_time_value.setText(_translate(
                "MainWindow", str(ventTimeValue)))
        else:
            self.vent_time_value.setText(_translate(
                "MainWindow", "N/A"))

        self.time_value.setText(_translate(
            "MainWindow", timeValue))
        
    ### INE2IALIZE UI ###

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "Woo Lab - COVID-19 Emergency Ventilation System"))
        self.ITV_value.setText(_translate("MainWindow", "0"))
        self.ITV_label.setText(_translate("MainWindow", "ITV (mL)"))
        self.E2I_button_pos.setText(_translate("MainWindow", "+"))
        self.E2I_label.setText(_translate(
            "MainWindow", "E:I (ratio)"))
        self.E2I_value.setText(_translate("MainWindow", str(self.E2I)))
        self.E2I_button_neg.setText(_translate("MainWindow", "-"))
        self.ETV_value.setText(_translate("MainWindow", "0"))
        self.ETV_label.setText(_translate("MainWindow", "ETV (mL)"))
        self.RR_button_neg.setText(_translate("MainWindow", "-"))
        self.RR_button_pos.setText(_translate("MainWindow", "+"))
        self.RR_label.setText(_translate("MainWindow", "RR (BPM)"))
        self.RR_value.setText(_translate("MainWindow", str(self.RR)))
        self.PEEP_value.setText(_translate("MainWindow", "5.2"))
        self.PEEP_label.setText(_translate("MainWindow", "PEEP (mmHg)"))
        self.sPEEP_value.setText(_translate("MainWindow", "2.0"))
        self.sPEEP_button_neg.setText(_translate("MainWindow", "-"))
        self.sPEEP_button_pos.setText(_translate("MainWindow", "+"))
        self.sPEEP_label.setText(_translate("MainWindow", "Set PEEP (mmHg)"))
        self.O2_value.setText(_translate("MainWindow", "28.3%"))
        self.O2_label.setText(_translate("MainWindow", "FiO2"))
        self.PIP_value.setText(_translate("MainWindow", "12.5"))
        self.PIP_label.setText(_translate("MainWindow", "Peak Pr (mmHg)"))
        self.sPIP_value.setText(_translate("MainWindow", "20.0"))
        self.sPIP_button_neg.setText(_translate("MainWindow", "-"))
        self.sPIP_button_pos.setText(_translate("MainWindow", "+"))
        self.sPIP_label.setText(_translate("MainWindow", "Set PIP (mmHg)"))
        self.PHASE_value.setText(_translate("MainWindow", "INS"))
        self.PHASE_label.setText(_translate("MainWindow", "System Phase"))
        self.time_label.setText(_translate("MainWindow", "Time"))
        self.record_button.setText(_translate("MainWindow", "•"))
        self.vent_time_label.setText(
            _translate("MainWindow", "Ventilation Time"))
        self.graph1_label.setText(_translate("MainWindow", "INS\n"
                                             "FLOW"))
        self.graph1_value.setText(_translate("MainWindow", "52.6"))
        self.graph1_units.setText(_translate("MainWindow", "SLPM"))
        self.graph2_label.setText(_translate("MainWindow", "EXP\n"
                                             "FLOW"))
        self.graph2_value.setText(_translate("MainWindow", "24.1"))
        self.graph2_units.setText(_translate("MainWindow", "SLPM"))
        self.graph3_label.setText(_translate("MainWindow", "LUNG\n"
                                             "PR"))
        self.graph3_value.setText(_translate("MainWindow", "12.8"))
        self.graph3_units.setText(_translate("MainWindow", "mmHg"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
