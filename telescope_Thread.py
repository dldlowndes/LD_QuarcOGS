import time

from PyQt5 import QtCore

import LD_Planewave
import LD_PWI_Status


class telescope_Thread(QtCore.QThread):
    """
    Do some work. Emit signals when results are ready
    """

    # Signals to carry the collected data out of the thread.
    # Separate so mode can
    # be easily toggled on/off.
    status_Signal = QtCore.pyqtSignal(LD_PWI_Status.LD_PWI_Status)

    def __init__(self):
        QtCore.QThread.__init__(self)

        # Flags.
        # Practically the thread will probably remain active whilever
        # the program is running.
        self.thread_Active = False
        
        self.mount = LD_Planewave.LD_Planewave()

    def Connect(self, ip_Address, port):
        self.mount.Connect_IP(ip_Address, port)
        self.thread_Active = True
        
    def Disconnect(self):
        self.thread_Active = False
        self.mount.Disconnect()

    def run(self):
        while self.thread_Active:
            status = self.mount.Status()
            self.status_Signal.emit(status)
            time.sleep(1)

    def stop(self):
        self.thread_Active = False
        self.wait()
