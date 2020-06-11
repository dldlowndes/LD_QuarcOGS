"""
Quarc OGS GUI

TODO:
    - Load TLEs from internet.
    - Load multiple TLE files to the same processing session
    - Figure out some way of live showing finder process.
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
        
        # Init various components
        self.Init_Defaults()
        self.Init_Threads()
        self.Init_Connections()
        
    def Init_Defaults(self):
        """
        Set some sensible defaults to populate the GUI. Help reduce the
        amount of typing.
        """
        
        # The TLE file name (Celestrak's visual list seems good enough)
        self.ui.value_Filename.setText("tle_Files/visual.txt")
        
        # Queens building. I'm making a statement.
        self.ui.value_Lat.setText("51.4566")
        self.ui.value_Lon.setText("-2.6020")
        self.ui.value_Height.setText("71")

        # Default is to start "tonight" and stop "tomorrow morning". Should be
        # a good enough starting point. As is processing every minute.
        t_now = datetime.datetime.now()
        t_start = datetime.datetime(t_now.year, t_now.month, t_now.day, 22, 00)
        t_stop = t_start + datetime.timedelta(hours=8)
        self.ui.date_Start.setDateTime(QtCore.QDateTime(t_start))
        self.ui.date_Stop.setDateTime(QtCore.QDateTime(t_stop))
        self.ui.value_Resolution.setValue(1)
        
        # 30 degrees high enough?
        self.ui.value_Degrees.setValue(30)

    def Init_Threads(self):    
        """
        Threads to do long lasting work that would hang the GUI.
        Make threads and signal/slot connections in here.
        """
        self.satellites_Thread = satellites_Thread.satellites_Thread()
        
        # For when the satellites thread has loaded some TLEs for passing to
        # the GUI
        self.satellites_Thread.tles_Signal.connect(self.On_TLEs_Signal)
        
        # For when the viable passes have been calculated.
        self.satellites_Thread.passes_Signal.connect(self.On_Passes_Signal)

    def Init_Connections(self):
        """
        Connect GUI elements to functions.        
        """

        self.ui.button_LoadFile.clicked.connect(self.On_Load_Button)
        self.ui.button_Search.clicked.connect(self.On_Search_Button)
        self.ui.button_Process.clicked.connect(self.On_Process_Button)
        
    def On_Load_Button(self):
        """
        Load a TLE list from file.
        """
        
        self.satellites_Thread.Load_List(self.ui.value_Filename.text())
        
    def On_Search_Button(self):
        """
        Search through the TLEs and return only those whose name contains
        the text in the search box
        """
        
        search = self.ui.value_Search.text()
        self.satellites_Thread.Search_List(search)
        
    def On_Process_Button(self):
        """
        Find the passes over the current site above some threshold alt.
        """
        
        # Site information
        self.satellites_Thread.lat = float(self.ui.value_Lat.text())
        self.satellites_Thread.lon = float(self.ui.value_Lon.text())
        self.satellites_Thread.height = float(self.ui.value_Height.text())
        
        # Times to search for passes within (and resolution)
        self.satellites_Thread.t_start = self.ui.date_Start.dateTime().toString(QtCore.Qt.ISODate)
        self.satellites_Thread.t_stop = self.ui.date_Stop.dateTime().toString(QtCore.Qt.ISODate)
        self.satellites_Thread.t_step = self.ui.value_Resolution.value()
        
        # Filter out passes that peak below this alt
        self.satellites_Thread.degrees = self.ui.value_Degrees.value()
        
        # Clear the passes table since we're about to start reprocessing.
        # Persisting data would be confusing since they might be for different
        # parameters than shown in the GUI
        self.ui.table_Passes.setRowCount(0)
        # Until I figure out a better way of showing process, just let the
        # user know this is doing something.
        self.ui.label_Status.setText("Status: Processing")
        # Actually do the processing.
        self.satellites_Thread.start()

    def On_TLEs_Signal(self, tle_List):
        """
        Display the TLE list contents in the GUI
        """
        
        # Clear table (since the TLE list is cleared anyway)
        self.ui.table_TLEs.setRowCount(0)
        
        # Fill table with new data.
        for i, tle in enumerate(tle_List):
            self.ui.table_TLEs.insertRow(i)
            self.ui.table_TLEs.setItem(i, 0, QtWidgets.QTableWidgetItem(tle.name))
            self.ui.table_TLEs.setItem(i, 1,  QtWidgets.QTableWidgetItem(tle[1]))
            self.ui.table_TLEs.setItem(i, 2, QtWidgets.QTableWidgetItem(tle[2]))
        
    
    def On_Passes_Signal(self, data):
        """
        Fill the table in the passes tab (and the graph tab?)
        """
        # No need to clear passes since the list is cleared when the processing
        # starts.
        
        # This signal means the processing is finished so update GUI to say.
        self.ui.label_Status.setText("Status: Inactive")
        
        # Fill the table with new data.
        for i, line in data.iterrows():
            self.ui.table_Passes.insertRow(i)
            self.ui.table_Passes.setItem(i, 0, QtWidgets.QTableWidgetItem(line.satellite)) #name
            self.ui.table_Passes.setItem(i, 1, QtWidgets.QTableWidgetItem(f"{line.alt:0.2f}")) #alt
            self.ui.table_Passes.setItem(i, 2, QtWidgets.QTableWidgetItem(line.time)) #time
            self.ui.table_Passes.setItem(i, 3, QtWidgets.QTableWidgetItem(f"{line.az:0.2f}")) #az
        

app = QtWidgets.QApplication([])

application = MyWindow()

application.show()

sys.exit(app.exec())
