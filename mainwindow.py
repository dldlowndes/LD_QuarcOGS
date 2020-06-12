# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.box_Telescope = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box_Telescope.sizePolicy().hasHeightForWidth())
        self.box_Telescope.setSizePolicy(sizePolicy)
        self.box_Telescope.setObjectName("box_Telescope")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.box_Telescope)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.box_MountSite = QtWidgets.QGroupBox(self.box_Telescope)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box_MountSite.sizePolicy().hasHeightForWidth())
        self.box_MountSite.setSizePolicy(sizePolicy)
        self.box_MountSite.setObjectName("box_MountSite")
        self.gridLayout_2.addWidget(self.box_MountSite, 0, 0, 1, 1)
        self.box_MountStatus = QtWidgets.QGroupBox(self.box_Telescope)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box_MountStatus.sizePolicy().hasHeightForWidth())
        self.box_MountStatus.setSizePolicy(sizePolicy)
        self.box_MountStatus.setObjectName("box_MountStatus")
        self.gridLayout_2.addWidget(self.box_MountStatus, 1, 0, 1, 1)
        self.box_Accessories = QtWidgets.QGroupBox(self.box_Telescope)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box_Accessories.sizePolicy().hasHeightForWidth())
        self.box_Accessories.setSizePolicy(sizePolicy)
        self.box_Accessories.setObjectName("box_Accessories")
        self.gridLayout_2.addWidget(self.box_Accessories, 2, 0, 1, 1)
        self.gridLayout_9.addWidget(self.box_Telescope, 0, 0, 1, 1)
        self.group_Satellites = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.group_Satellites.sizePolicy().hasHeightForWidth())
        self.group_Satellites.setSizePolicy(sizePolicy)
        self.group_Satellites.setObjectName("group_Satellites")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.group_Satellites)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.group_SatCalc = QtWidgets.QGroupBox(self.group_Satellites)
        self.group_SatCalc.setObjectName("group_SatCalc")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.group_SatCalc)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.tabs_Calculator = QtWidgets.QTabWidget(self.group_SatCalc)
        self.tabs_Calculator.setObjectName("tabs_Calculator")
        self.tab_TLEs = QtWidgets.QWidget()
        self.tab_TLEs.setObjectName("tab_TLEs")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_TLEs)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_15 = QtWidgets.QGridLayout()
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.button_LoadFile = QtWidgets.QPushButton(self.tab_TLEs)
        self.button_LoadFile.setObjectName("button_LoadFile")
        self.gridLayout_11.addWidget(self.button_LoadFile, 0, 2, 1, 1)
        self.label_Filename = QtWidgets.QLabel(self.tab_TLEs)
        self.label_Filename.setObjectName("label_Filename")
        self.gridLayout_11.addWidget(self.label_Filename, 0, 0, 1, 1)
        self.value_Filename = QtWidgets.QLineEdit(self.tab_TLEs)
        self.value_Filename.setObjectName("value_Filename")
        self.gridLayout_11.addWidget(self.value_Filename, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem, 0, 3, 1, 1)
        self.label_Search = QtWidgets.QLabel(self.tab_TLEs)
        self.label_Search.setObjectName("label_Search")
        self.gridLayout_11.addWidget(self.label_Search, 1, 0, 1, 1)
        self.value_Search = QtWidgets.QLineEdit(self.tab_TLEs)
        self.value_Search.setObjectName("value_Search")
        self.gridLayout_11.addWidget(self.value_Search, 1, 1, 1, 1)
        self.button_Search = QtWidgets.QPushButton(self.tab_TLEs)
        self.button_Search.setObjectName("button_Search")
        self.gridLayout_11.addWidget(self.button_Search, 1, 2, 1, 1)
        self.gridLayout_15.addLayout(self.gridLayout_11, 0, 0, 1, 1)
        self.table_TLEs = QtWidgets.QTableWidget(self.tab_TLEs)
        self.table_TLEs.setObjectName("table_TLEs")
        self.table_TLEs.setColumnCount(3)
        self.table_TLEs.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_TLEs.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_TLEs.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_TLEs.setHorizontalHeaderItem(2, item)
        self.gridLayout_15.addWidget(self.table_TLEs, 1, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_15, 0, 0, 1, 1)
        self.tabs_Calculator.addTab(self.tab_TLEs, "")
        self.tab_Passes = QtWidgets.QWidget()
        self.tab_Passes.setObjectName("tab_Passes")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.tab_Passes)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.box_Site = QtWidgets.QGroupBox(self.tab_Passes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box_Site.sizePolicy().hasHeightForWidth())
        self.box_Site.setSizePolicy(sizePolicy)
        self.box_Site.setObjectName("box_Site")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.box_Site)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_Lat = QtWidgets.QLabel(self.box_Site)
        self.label_Lat.setObjectName("label_Lat")
        self.gridLayout_4.addWidget(self.label_Lat, 0, 0, 1, 1)
        self.value_Lat = QtWidgets.QLineEdit(self.box_Site)
        self.value_Lat.setObjectName("value_Lat")
        self.gridLayout_4.addWidget(self.value_Lat, 0, 1, 1, 1)
        self.label_Lon = QtWidgets.QLabel(self.box_Site)
        self.label_Lon.setObjectName("label_Lon")
        self.gridLayout_4.addWidget(self.label_Lon, 1, 0, 1, 1)
        self.value_Lon = QtWidgets.QLineEdit(self.box_Site)
        self.value_Lon.setObjectName("value_Lon")
        self.gridLayout_4.addWidget(self.value_Lon, 1, 1, 1, 1)
        self.label_Height = QtWidgets.QLabel(self.box_Site)
        self.label_Height.setObjectName("label_Height")
        self.gridLayout_4.addWidget(self.label_Height, 2, 0, 1, 1)
        self.value_Height = QtWidgets.QLineEdit(self.box_Site)
        self.value_Height.setObjectName("value_Height")
        self.gridLayout_4.addWidget(self.value_Height, 2, 1, 1, 1)
        self.horizontalLayout_3.addWidget(self.box_Site)
        self.box_Time = QtWidgets.QGroupBox(self.tab_Passes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box_Time.sizePolicy().hasHeightForWidth())
        self.box_Time.setSizePolicy(sizePolicy)
        self.box_Time.setObjectName("box_Time")
        self.gridLayout = QtWidgets.QGridLayout(self.box_Time)
        self.gridLayout.setObjectName("gridLayout")
        self.date_Start = QtWidgets.QDateTimeEdit(self.box_Time)
        self.date_Start.setObjectName("date_Start")
        self.gridLayout.addWidget(self.date_Start, 0, 1, 1, 1)
        self.label_StartTime = QtWidgets.QLabel(self.box_Time)
        self.label_StartTime.setObjectName("label_StartTime")
        self.gridLayout.addWidget(self.label_StartTime, 0, 0, 1, 1)
        self.date_Stop = QtWidgets.QDateTimeEdit(self.box_Time)
        self.date_Stop.setObjectName("date_Stop")
        self.gridLayout.addWidget(self.date_Stop, 1, 1, 1, 1)
        self.label_StopTime = QtWidgets.QLabel(self.box_Time)
        self.label_StopTime.setObjectName("label_StopTime")
        self.gridLayout.addWidget(self.label_StopTime, 1, 0, 1, 1)
        self.label_Resolution = QtWidgets.QLabel(self.box_Time)
        self.label_Resolution.setObjectName("label_Resolution")
        self.gridLayout.addWidget(self.label_Resolution, 2, 0, 1, 1)
        self.value_Resolution = QtWidgets.QDoubleSpinBox(self.box_Time)
        self.value_Resolution.setObjectName("value_Resolution")
        self.gridLayout.addWidget(self.value_Resolution, 2, 1, 1, 1)
        self.horizontalLayout_3.addWidget(self.box_Time)
        self.box_Process = QtWidgets.QGroupBox(self.tab_Passes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box_Process.sizePolicy().hasHeightForWidth())
        self.box_Process.setSizePolicy(sizePolicy)
        self.box_Process.setObjectName("box_Process")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.box_Process)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.button_Process = QtWidgets.QPushButton(self.box_Process)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_Process.sizePolicy().hasHeightForWidth())
        self.button_Process.setSizePolicy(sizePolicy)
        self.button_Process.setObjectName("button_Process")
        self.gridLayout_10.addWidget(self.button_Process, 3, 0, 1, 1)
        self.label_Status = QtWidgets.QLabel(self.box_Process)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Status.sizePolicy().hasHeightForWidth())
        self.label_Status.setSizePolicy(sizePolicy)
        self.label_Status.setObjectName("label_Status")
        self.gridLayout_10.addWidget(self.label_Status, 4, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_Degrees = QtWidgets.QLabel(self.box_Process)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Degrees.sizePolicy().hasHeightForWidth())
        self.label_Degrees.setSizePolicy(sizePolicy)
        self.label_Degrees.setObjectName("label_Degrees")
        self.horizontalLayout_4.addWidget(self.label_Degrees)
        self.value_Degrees = QtWidgets.QDoubleSpinBox(self.box_Process)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.value_Degrees.sizePolicy().hasHeightForWidth())
        self.value_Degrees.setSizePolicy(sizePolicy)
        self.value_Degrees.setObjectName("value_Degrees")
        self.horizontalLayout_4.addWidget(self.value_Degrees)
        self.gridLayout_10.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)
        self.horizontalLayout_3.addWidget(self.box_Process)
        self.gridLayout_13.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.table_Passes = QtWidgets.QTableWidget(self.tab_Passes)
        self.table_Passes.setObjectName("table_Passes")
        self.table_Passes.setColumnCount(4)
        self.table_Passes.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_Passes.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_Passes.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_Passes.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_Passes.setHorizontalHeaderItem(3, item)
        self.gridLayout_13.addWidget(self.table_Passes, 1, 0, 1, 1)
        self.tabs_Calculator.addTab(self.tab_Passes, "")
        self.tab_Graph = QtWidgets.QWidget()
        self.tab_Graph.setObjectName("tab_Graph")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.tab_Graph)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.layout_Graph = QtWidgets.QGridLayout()
        self.layout_Graph.setObjectName("layout_Graph")
        self.gridLayout_14.addLayout(self.layout_Graph, 0, 0, 1, 1)
        self.tabs_Calculator.addTab(self.tab_Graph, "")
        self.gridLayout_7.addWidget(self.tabs_Calculator, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.group_SatCalc, 0, 0, 1, 1)
        self.group_SatQueue = QtWidgets.QGroupBox(self.group_Satellites)
        self.group_SatQueue.setObjectName("group_SatQueue")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.group_SatQueue)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableWidget_3 = QtWidgets.QTableWidget(self.group_SatQueue)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(3)
        self.tableWidget_3.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(2, item)
        self.gridLayout_3.addWidget(self.tableWidget_3, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.group_SatQueue)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.group_SatQueue)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.pushButton_2 = QtWidgets.QPushButton(self.group_SatQueue)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.group_SatQueue, 1, 0, 1, 1)
        self.gridLayout_9.addWidget(self.group_Satellites, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabs_Calculator.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.box_Telescope.setTitle(_translate("MainWindow", "Telescope Mount Status"))
        self.box_MountSite.setTitle(_translate("MainWindow", "Site"))
        self.box_MountStatus.setTitle(_translate("MainWindow", "Mount"))
        self.box_Accessories.setTitle(_translate("MainWindow", "Accessories"))
        self.group_Satellites.setTitle(_translate("MainWindow", "Satellites"))
        self.group_SatCalc.setTitle(_translate("MainWindow", "Pass Calculator"))
        self.button_LoadFile.setText(_translate("MainWindow", "Load File"))
        self.label_Filename.setText(_translate("MainWindow", "TLEs File name:"))
        self.label_Search.setText(_translate("MainWindow", "Search names:"))
        self.button_Search.setText(_translate("MainWindow", "Filter"))
        item = self.table_TLEs.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Line 1"))
        item = self.table_TLEs.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Line 2"))
        item = self.table_TLEs.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Line 3"))
        self.tabs_Calculator.setTabText(self.tabs_Calculator.indexOf(self.tab_TLEs), _translate("MainWindow", "TLE List"))
        self.box_Site.setTitle(_translate("MainWindow", "Observation Co-ordinates"))
        self.label_Lat.setText(_translate("MainWindow", "Lat"))
        self.label_Lon.setText(_translate("MainWindow", "Lon"))
        self.label_Height.setText(_translate("MainWindow", "Height"))
        self.box_Time.setTitle(_translate("MainWindow", "Search parameters"))
        self.label_StartTime.setText(_translate("MainWindow", "Start Time"))
        self.label_StopTime.setText(_translate("MainWindow", "Stop Time"))
        self.label_Resolution.setText(_translate("MainWindow", "Resolution (mins)"))
        self.box_Process.setTitle(_translate("MainWindow", "Processing"))
        self.button_Process.setText(_translate("MainWindow", "Find Passes"))
        self.label_Status.setText(_translate("MainWindow", "Status: Inactive"))
        self.label_Degrees.setText(_translate("MainWindow", "Filter Alt (°)"))
        item = self.table_Passes.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Satellite Name"))
        item = self.table_Passes.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Max altitude"))
        item = self.table_Passes.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Time of max alt"))
        item = self.table_Passes.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Az at max alt"))
        self.tabs_Calculator.setTabText(self.tabs_Calculator.indexOf(self.tab_Passes), _translate("MainWindow", "Passes"))
        self.tabs_Calculator.setTabText(self.tabs_Calculator.indexOf(self.tab_Graph), _translate("MainWindow", "Graph"))
        self.group_SatQueue.setTitle(_translate("MainWindow", "Queue"))
        item = self.tableWidget_3.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Satelite Name"))
        item = self.tableWidget_3.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Track Start"))
        item = self.tableWidget_3.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Track Stop"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
