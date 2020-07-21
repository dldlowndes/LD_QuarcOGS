import logging

from PyQt5 import QtCore

import LD_TLEList
import LD_PassFinder

log = logging.getLogger(__name__)

class satellites_Thread(QtCore.QThread):
    """
    Do some work. Emit signals when results are ready
    """

    # Signals to carry the collected data out of the thread.
    # Separate so mode can
    # be easily toggled on/off.
    tles_Signal = QtCore.pyqtSignal(list)
    passes_Signal = QtCore.pyqtSignal(list)

    def __init__(self):
        QtCore.QThread.__init__(self)

        log.debug("Init thread defaults")
        # Flags.
        # Practically the thread will probably remain active whilever
        # the program is running.
        self.thread_Active = False

        self.my_TLE_List = []
        self.lat = None
        self.lon = None
        self.height = None
        self.t_start = None
        self.t_stop = None
        self.t_step = None

        self.degrees = 0

        self.my_TLE_List = LD_TLEList.LD_TLEList()
        self.finder = LD_PassFinder.LD_PassFinder()


    def Load_List(self, filename, internet, append=False):
        log.debug(f"Load TLE list {filename}, append? {append}")
        if internet:
            self.my_TLE_List.Load_TLEs_From_URL(filename, append)
        else:
            self.my_TLE_List.Load_TLEs_From_File(filename, append)
        self.finder.Load_TLE_Data(self.my_TLE_List)
        self.tles = self.finder.Search_TLE_Data("")
        self.tles_Signal.emit(self.tles)

    def Search_List(self, search):
        log.debug(f"Search TLE list for {search}.")
        self.tles = self.finder.Search_TLE_Data(search)
        self.tles_Signal.emit(self.tles)

    def run(self):
        log.debug("Start pass finder thread")
        self.finder.Set_Position(self.lat, self.lon, self.height)
        self.finder.Search_Time_Range(self.t_start, self.t_stop, self.t_step)

        self.finder.Calculate_Passes(self.tles)
        self.pass_Data = self.finder.Filter_Passes(alt_Filter=self.degrees)
        self.finder.Save_Pass_List()

        self.passes_Signal.emit(self.pass_Data)

    def stop(self):
        log.debug("Stop pass finder thread")
        self.thread_Active = False
        self.wait()
