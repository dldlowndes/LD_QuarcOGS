"""
Quarc OGS GUI

TODO:
    - Load TLEs from internet.
    - Load multiple TLE files to the same processing session
    - Figure out some way of live showing finder process.
    - Pretty up the plot.
    - Convert LST to "real" time
    - Allow raw commands to be sent to the telescope.
    
"""

# pylint: disable=C0103
# pylint: disable=R0902

import datetime
import sys

from PyQt5 import QtWidgets, QtCore
import matplotlib
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import tzlocal

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
        self.Init_Plot()

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
        t_start = t_now #datetime.datetime(t_now.year, t_now.month, t_now.day, 22, 00)
        t_stop = t_start + datetime.timedelta(hours=2)
        self.ui.date_Start.setDateTime(QtCore.QDateTime(t_start))
        self.ui.date_Stop.setDateTime(QtCore.QDateTime(t_stop))
        self.ui.value_Resolution.setValue(1)

        # 30 degrees high enough?
        self.ui.value_Degrees.setValue(30)
        
        # The telescope is *probably* connected to the local machine.
        self.ui.value_ip.setText("http://127.0.0.1")
        self.ui.value_port.setText("8220")

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
        
        # Controls the telescope.
        self.telescope_Thread = telescope_Thread.telescope_Thread()
        
        # Update of the telescope status. I suppose this will emit quite
        # frequently.
        self.telescope_Thread.status_Signal.connect(self.On_Telescope_Status)
        self.telescope_Thread.waiting_Signal.connect(self.On_Waiting_Update)

    def Init_Connections(self):
        """
        Connect GUI elements to functions.
        """

        self.ui.button_LoadFile.clicked.connect(self.On_Load_Button)
        self.ui.button_Search.clicked.connect(self.On_Search_Button)
        self.ui.button_Process.clicked.connect(self.On_Process_Button)
        
        self.ui.button_Connect.clicked.connect(self.On_Connect_Button)
        self.ui.button_latlon_auto.clicked.connect(self.On_LatLon_Auto)
        
        self.ui.button_tle_track.clicked.connect(self.On_TLE_Track_Button)
        self.ui.button_goto_altaz.clicked.connect(self.On_Goto_AltAz_Button)
        self.ui.button_goto_radec.clicked.connect(self.On_Goto_RaDec_Button)
        
        self.ui.table_Passes.doubleClicked.connect(self.On_Pass_Click)
        self.ui.table_Waiting.doubleClicked.connect(self.On_Waiting_Click)
        self.ui.table_TLEs.doubleClicked.connect(self.On_TLE_Click)
        

    def Init_Plot(self):
        """
        Make the canvas and set some things that can be set at init time
        (which turns out to be not a lot!)
        """

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.ui.layout_Graph.addWidget(NavigationToolbar(self.canvas, self))
        self.ui.layout_Graph.addWidget(self.canvas)
        self.axes = self.canvas.figure.subplots()
        self.canvas.figure.subplots_adjust(left=0.05,
                                           right=0.95,
                                           top=0.98,
                                           bottom=0.175)

    def Update_Plot(self, pass_Data):
        """
        Plot all the passes on a graph window. alt against time for each sat
        that fulfilled the criteria of Filter_Passes in the satellites_Thread.
        """

        self.axes.xaxis_date(self.satellites_Thread.finder.my_tz)
        #fmt = matplotlib.dates.DateFormatter("%Y/%m/%d %H:%M")
        fmt = matplotlib.dates.DateFormatter("%H:%M")
        self.axes.xaxis.set_major_formatter(fmt)

        # Get the axes looking nice.
        self.axes.xaxis.set_major_locator(matplotlib.dates.MinuteLocator(interval=30))
        self.axes.grid(True, which="major", axis="both", linestyle="--")

        self.axes.xaxis.set_minor_locator(matplotlib.dates.MinuteLocator(interval=5))
        self.axes.grid(True, which="minor", axis="both", linestyle=":")

        self.axes.xaxis.set_tick_params(rotation=90)

        self.axes.set_ylim(0, 90)
        self.axes.set_xlim(self.satellites_Thread.finder.t_start.plot_date,
                           self.satellites_Thread.finder.t_stop.plot_date)

        for sat, peak_Info, data in pass_Data:
            # Make timestamps that matplotlib can understand.
            x_data = [x.plot_date for x in data["time"].values]
            # Altitude is the only particularly interesting feature for these
            # purposes (plotting azimuth as well would be confusing)
            y_data = data["alt"]
            self.axes.plot_date(x_data, y_data, xdate=True,
                                linestyle="-", marker=None)

            label_text = sat.name.rstrip()
            label_pos_x = matplotlib.dates.date2num(peak_Info[0])
            label_pos_y = peak_Info[1]

            self.axes.text(label_pos_x, label_pos_y, label_text)

        self.canvas.draw()

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
        # parameters than shown in the GUI.
        # Also clear the plot.
        self.ui.table_Passes.setRowCount(0)
        self.axes.clear()
        self.canvas.draw()
        # Until I figure out a better way of showing process, just let the
        # user know this is doing something.
        self.ui.label_Status.setText("Status: Processing")
        # Actually do the processing.
        self.satellites_Thread.start()

    def On_LatLon_Auto(self):
        """
        Get the lat/lon from the mount if possible.
        """

        mount_lat = self.ui.value_telescope_lat.text()
        mount_lon = self.ui.value_telescope_lon.text()
        mount_height = self.ui.value_telescope_height.text()

        self.ui.value_Lat.setText(mount_lat)
        self.ui.value_Lon.setText(mount_lon)
        self.ui.value_Height.setText(mount_height)

    def On_Goto_AltAz_Button(self):
        """
        Instruct the telescope mount to go to a specific alt/az
        """
        
        alt = float(self.ui.value_alt_cmd.text())
        az = float(self.ui.value_az_cmd.text())

        self.telescope_Thread.Move_AltAz(alt, az)

    def On_Goto_RaDec_Button(self):
        """
        Instruct the telescope mount to go to a specific ra/dec in the
        specified coordinate system (apparent or j2000)
        """
        
        ra = float(self.ui.value_ra_cmd.text())
        dec = float(self.ui.value_dec_cmd.text())
        j2000 = self.ui.option_cmd_j2000.isChecked()

        self.telescope_Thread.Move_RaDec(ra, dec, j2000)
        
    def On_TLE_Track_Button(self):
        tle = self.ui.value_tle_cmd.toPlainText()
        
        if self.ui.option_tle_cmd_now.isChecked():
            self.telescope_Thread.Follow_TLE(tle)
        else:
            time = self.ui.value_tle_cmd_start.dateTime().toPyDateTime()
            print(time)
            self.telescope_Thread.Add_Waiting_TLE(tle, time, time)

    def On_TLEs_Signal(self, tle_List):
        """
        Display the TLE list contents in the GUI
        """

        # Clear table (since the TLE list is cleared anyway)
        self.ui.table_TLEs.setRowCount(0)

        # Fill table with new data.
        for i, tle in enumerate(tle_List):
            self.ui.table_TLEs.insertRow(i)
            self.ui.table_TLEs.setItem(i, 0, QtWidgets.QTableWidgetItem(tle.name.rstrip()))
            self.ui.table_TLEs.setItem(i, 1, QtWidgets.QTableWidgetItem(tle[1]))
            self.ui.table_TLEs.setItem(i, 2, QtWidgets.QTableWidgetItem(tle[2]))

    def On_Passes_Signal(self, pass_Data):
        """
        Fill the table in the passes tab (and the graph tab?)
        """
        # No need to clear passes since the list is cleared when the processing
        # starts.

        # This signal means the processing is finished so update GUI to say.
        self.ui.label_Status.setText("Status: Inactive")

        # Fill the table with new data.
        for i, sat in enumerate(pass_Data):
            name = sat[0].name.rstrip()
            time = str(sat[1][0])
            alt = sat[1][1]
            az = sat[1][2]
            self.ui.table_Passes.insertRow(i)
            self.ui.table_Passes.setItem(i, 0, QtWidgets.QTableWidgetItem(name))
            self.ui.table_Passes.setItem(i, 1, QtWidgets.QTableWidgetItem(f"{alt:0.2f}"))
            self.ui.table_Passes.setItem(i, 2, QtWidgets.QTableWidgetItem(time))
            self.ui.table_Passes.setItem(i, 3, QtWidgets.QTableWidgetItem(f"{az:0.2f}"))

        self.Update_Plot(pass_Data)

    def On_Connect_Button(self):
        """
        Connect to the telescope HTTP server based on the IP address specified.
        """
        ip = self.ui.value_ip.text()
        port = self.ui.value_port.text()
        self.telescope_Thread.Connect(ip, port)
        self.telescope_Thread.start()

    def On_Telescope_Status(self, pwi_Status):
        """
        The telescope periodically emits its status, update the GUI with the
        new data.
        """

        self.ui.value_telescope_lat.setText(f"{pwi_Status.site.latitude}")
        self.ui.value_telescope_lon.setText(f"{pwi_Status.site.longitude}")
        self.ui.value_telescope_height.setText(f"{pwi_Status.site.height}")
        lst = pwi_Status.site.lst
        
        self.ui.value_lst.setText(lst)
        
        self.ui.value_alt_status.setText(f"{pwi_Status.mount.altitude}")
        self.ui.value_az_status.setText(f"{pwi_Status.mount.azimuth}")
        if self.ui.option_j2000_status.isChecked():
            self.ui.value_ra_status.setText(f"{pwi_Status.mount.ra_apparent}")
            self.ui.value_dec_status.setText(f"{pwi_Status.mount.dec_apparent}")
        else:
            self.ui.value_ra_status.setText(f"{pwi_Status.mount.ra_j2000}")
            self.ui.value_dec_status.setText(f"{pwi_Status.mount.dec_j2000}")
        
        self.ui.value_a0_enabled.setText(f"{pwi_Status.mount.axis0.is_enabled}")
        self.ui.value_a0_rms.setText(f"{pwi_Status.mount.axis0.rms_error}")
        self.ui.value_a0_dist.setText(f"{pwi_Status.mount.axis0.dist_to_target}")
        self.ui.value_a0_servo.setText(f"{pwi_Status.mount.axis0.servo_error}")
        self.ui.value_a0_position.setText(f"{pwi_Status.mount.axis0.position}")

        self.ui.value_a1_enabled.setText(f"{pwi_Status.mount.axis1.is_enabled}")
        self.ui.value_a1_rms.setText(f"{pwi_Status.mount.axis1.rms_error}")
        self.ui.value_a1_dist.setText(f"{pwi_Status.mount.axis1.dist_to_target}")
        self.ui.value_a1_servo.setText(f"{pwi_Status.mount.axis1.servo_error}")
        self.ui.value_a1_position.setText(f"{pwi_Status.mount.axis1.position}")
        
        self.ui.value_Geometry.setText(f"{pwi_Status.mount.geometry}")
        slewing = pwi_Status.mount.is_slewing
        tracking = pwi_Status.mount.is_tracking
        self.ui.value_MoveStatus.setText(f"Slewing:{slewing}, Tracking:{tracking}")
        
    def On_Pass_Click(self, rowcol):
        """
        Clicking on a pass in the pass list adds it to a queue, when the pass
        gets close (in time), the telescope will track it.
        Refuses to add TLEs where the calculated pass data is minimal (so the
        start and stop time are the same) - likely these passes wouldn't be of
        any interesting use anyway.
        """
        
        # The signal from the table gives the ID of the element clicked so get
        # the corresponding TLE and pass data for this.
        line = self.satellites_Thread.pass_Data[rowcol.row()]
        tle = line[0]

        # Check it's a worthwhile pass
        if len(line[2]) > 1:
            # Get the time the satellite goes above/below the horizon. (even
            # if there's an alt filter in the pass finder, this way the
            # telescope will definitely have found the satellite by the time
            # it's nice and high in the sky)            
            start = line[2].iloc[0].time.to_datetime(tzlocal.get_localzone())
            stop = line[2].iloc[-1].time.to_datetime(tzlocal.get_localzone())

            # Let the telescope thread know about the waiting pass.
            # (satellite thread then emits which is captured by On_Waiting_Update)
            self.telescope_Thread.Add_Waiting_TLE(tle, start, stop)
        else:
            print("""Insufficient data for pass, it's probably barely over the
                  horizon. Not added to tracking queue.""")
        
    def On_Waiting_Click(self, rowcol):
        """
        Clicking on a pass in the waiting list will remove it (and cancel it)
        """
        
        # Get the clicked element's row and tell the telescope thread which
        # row it was. self.On_Waiting_Update ensures that the table row number
        # and the internal list element number correspond to each other.
        row = rowcol.row()
        self.telescope_Thread.Remove_Waiting_TLE(row)
    
    def On_TLE_Click(self, rowcol):
        row = rowcol.row()
        tle = self.satellites_Thread.my_TLE_List[row]
        
        self.ui.value_tle_cmd.setPlainText(str(tle))
    
    def On_Waiting_Update(self, waiting_List):
        """
        In order to keep track of the elements in the waiting list, redraw it
        whenever it changes. I guess this would be a bad idea if it were a
        more updated element but realistically it's not going to get hit that
        hard.
        """
        
        self.ui.table_Waiting.setRowCount(0)
        for i, row in enumerate(waiting_List):
            name = row[0].name
            start = row[1]
            stop = row[2]
            self.ui.table_Waiting.insertRow(i)
            self.ui.table_Waiting.setItem(i, 0, QtWidgets.QTableWidgetItem(name))
            self.ui.table_Waiting.setItem(i, 1, QtWidgets.QTableWidgetItem(f"{start}"))
            self.ui.table_Waiting.setItem(i, 2, QtWidgets.QTableWidgetItem(f"{stop}"))
        
        

app = QtWidgets.QApplication([])

application = MyWindow()

application.show()

sys.exit(app.exec())
