import time

from PyQt5 import QtCore

import pandas as pd

import LD_TLEList
import LD_PassFinder

class satellites_Thread(QtCore.QThread):
    """
    Do some work. Emit signals when results are ready
    """

    # Signals to carry the collected data out of the thread.
    # Separate so mode can
    # be easily toggled on/off.
    tles_Signal = QtCore.pyqtSignal(list)
    passes_Signal = QtCore.pyqtSignal(pd.DataFrame)

    def __init__(self):
        QtCore.QThread.__init__(self)

        # Flags.
        # Practically the thread will probably remain active whilever
        # the program is running.
        self.thread_Active = False      
        
        self.my_TLE_List = None
        self.lat = None
        self.lon = None
        self.height = None
        self.t_start = None
        self.t_stop = None
        self.t_step = None
        
        self.degrees = 0
        
        self.finder = LD_PassFinder.LD_PassFinder()
        
    def Load_List(self, filename):
        self.my_TLE_List = LD_TLEList.LD_TLE_List(filename, False)
        self.tles_Signal.emit(list(self.my_TLE_List.TLEs))

    def run(self):
        self.finder.Set_Position(self.lat, self.lon, self.height)
        self.finder.Search_Time_Range(self.t_start, self.t_stop, self.t_step)
        self.finder.Load_TLE_Data(self.my_TLE_List)
        
        self.finder.Calculate_Passes()
        self.finder.Filter_Passes(alt_Filter = self.degrees)
        
        data = self.finder.Get_Pass_List()

        self.passes_Signal.emit(data)

    def stop(self):
        self.thread_Active = False
        self.wait()

    def On_Load_TLEs(self):
        pass
    
    def On_Calculate_Passes(self):
        pass