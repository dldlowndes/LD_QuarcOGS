"""
Quarc OGS GUI
"""

# pylint: disable=C0103
# pylint: disable=R0902

import datetime
import sys

from PyQt5 import QtWidgets, QtCore, QtGui
import mainwindow
import satellites_Thread
import telescope_Thread

class MyWindow(QtWidgets.QMainWindow):
    """
    Window for the UI for the OGS program.
    """
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.Init_Defaults()
        self.Init_Threads()
        self.Init_Connections()
        
    def Init_Defaults(self):
        self.ui.value_Filename.setText("tle_Files/visual.txt")
        
        self.ui.value_Lat.setText("51.4566")
        self.ui.value_Lon.setText("-2.6020")
        self.ui.value_Height.setText("71")

        t_now = datetime.datetime.now()
        t_start = datetime.datetime(t_now.year, t_now.month, t_now.day, 22, 00)
        t_stop = t_start + datetime.timedelta(hours=8)
        self.ui.date_Start.setDateTime(QtCore.QDateTime(t_start))
        self.ui.date_Stop.setDateTime(QtCore.QDateTime(t_stop))
        self.ui.value_Resolution.setValue(1)
        self.ui.value_Degrees.setValue(30)

    def Init_Threads(self):     
        self.satellites_Thread = satellites_Thread.satellites_Thread()
        self.satellites_Thread.tles_Signal.connect(self.On_TLEs_Signal)
        self.satellites_Thread.passes_Signal.connect(self.On_Passes_Signal)


    def Init_Connections(self):
        self.ui.button_LoadFile.clicked.connect(self.On_Load_Button)
        self.ui.button_Search.clicked.connect(self.On_Search_Button)
        self.ui.button_Process.clicked.connect(self.On_Process_Button)
        
    def On_Load_Button(self):
        self.satellites_Thread.Load_List(self.ui.value_Filename.text())
        
    def On_Search_Button(self):
        search = self.ui.value_Search.text()
        self.satellites_Thread.Search_List(search)
        
    def On_Process_Button(self):
        self.satellites_Thread.lat = float(self.ui.value_Lat.text())
        self.satellites_Thread.lon = float(self.ui.value_Lon.text())
        self.satellites_Thread.height = float(self.ui.value_Height.text())
        
        self.satellites_Thread.t_start = self.ui.date_Start.dateTime().toString(QtCore.Qt.ISODate)
        self.satellites_Thread.t_stop = self.ui.date_Stop.dateTime().toString(QtCore.Qt.ISODate)
        self.satellites_Thread.t_step = self.ui.value_Resolution.value()
        
        self.satellites_Thread.degrees = self.ui.value_Degrees.value()
        
        self.ui.table_Passes.setRowCount(0)
        self.ui.label_Status.setText("Status: Processing")
        self.satellites_Thread.start()
        
        

    def On_TLEs_Signal(self, tle_List):
        """
        Display the TLE list contents in the GUI
        """
        
        self.ui.table_TLEs.setRowCount(0)
        
        for i, tle in enumerate(tle_List):
            self.ui.table_TLEs.insertRow(i)
            self.ui.table_TLEs.setItem(i, 0, QtWidgets.QTableWidgetItem(tle.name))
            self.ui.table_TLEs.setItem(i, 1,  QtWidgets.QTableWidgetItem(tle[1]))
            self.ui.table_TLEs.setItem(i, 2, QtWidgets.QTableWidgetItem(tle[2]))
        
    
    def On_Passes_Signal(self, data):
        """
        Fill the table in the passes tab (and the graph tab?)
        """
        self.ui.label_Status.setText("Status: Inactive")
        
        for i, line in data.iterrows():
            self.ui.table_Passes.insertRow(i)
            print(f"{line.satellite}, {line.alt}, {line.time}, {line.az}")
            self.ui.table_Passes.setItem(i, 0, QtWidgets.QTableWidgetItem(line.satellite)) #name
            self.ui.table_Passes.setItem(i, 1, QtWidgets.QTableWidgetItem(f"{line.alt:0.2f}")) #alt
            self.ui.table_Passes.setItem(i, 2, QtWidgets.QTableWidgetItem(line.time)) #time
            self.ui.table_Passes.setItem(i, 3, QtWidgets.QTableWidgetItem(f"{line.az:0.2f}")) #az
        
    
        

app = QtWidgets.QApplication([])

application = MyWindow()

application.show()

sys.exit(app.exec())
