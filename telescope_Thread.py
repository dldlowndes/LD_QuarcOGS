import datetime
import functools
import time

import tzlocal

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
    waiting_Signal = QtCore.pyqtSignal(list)

    def __init__(self):
        QtCore.QThread.__init__(self)

        # Flags.
        # Practically the thread will probably remain active whilever
        # the program is running.
        self.thread_Active = False

        self.mount = LD_Planewave.LD_Planewave()

        self.waiting_List = []

    def Connect(self, ip_Address, port):
        """
        Connect to the telescope HTTP server and tell the HTTP server to
        connect to the physical hardware.
        TODO: And enable axes?
        """

        self.mount.Connect_IP(ip_Address, port)
        self.thread_Active = True
        self.mount.Connect()

    def Disconnect(self):
        """
        Disconnect from the telescope
        TODO: And disable axes?
        """

        self.thread_Active = False
        self.mount.Disconnect()

    def Add_Waiting_TLE(self, tle, start, stop):
        """
        Add a TLE to the waiting list of TLEs to track. Use a QTimer to fire
        the TLE tracking function at (roughly) "start".
        "stop" is just used for displaying the pass stop time to the user.
        """

        # Get the time until the TLE's pass start in ms (which is how the 
        # QTimer likes it).
        now = datetime.datetime.now(tzlocal.get_localzone())
        delta = start - now
        delta_ms = delta.total_seconds() * 1000.0

        # Only bother if the pass is actually in the future.
        if delta_ms > 0:
            # Make a timer to go off when the TLE is due.
            timer = QtCore.QTimer(self)
            timer.timeout.connect(functools.partial(self.Triggered_Follow_TLE, tle))
            timer.setSingleShot(True)
            print(f"start {start} added at {now}, which is {delta_ms} away")
            timer.start(delta_ms)

            # Add the info to a list to keep track of all the timers.
            # Keep the list sorted for clarity
            self.waiting_List.append([tle, start, stop, timer])
            self.waiting_List.sort(key=lambda x: x[1])

            # Emit the list so the GUI can update.
            self.waiting_Signal.emit(self.waiting_List)
        elif (now < stop):
            print(f"Error? pass already started. tracking remainder of it")
            self.Follow_TLE(tle)
        else:
            print(f"Error, pass has already happened.")

    def Remove_Waiting_TLE(self, index):
        """
        Remove a TLE from the waiting list (maybe it was added by accident?)
        and stop the follow command from being fired.
        """

        # Stop the timer from the selected row
        self.waiting_List[index][3].stop()
        # Remove selected row
        self.waiting_List.pop(index)

        # Send a signal so the GUI updates.
        self.waiting_Signal.emit(self.waiting_List)

    def Triggered_Follow_TLE(self, tle):
        """
        Does this work? If the follow tle was triggered by a QTimer, it must be
        the first one in the waiting list? If so we can remove it, update the
        GUI and trigger the actual follow command
        """
        self.waiting_List.pop(0)
        self.waiting_Signal.emit(self.waiting_List)

        self.Follow_TLE(tle)

    def Follow_TLE(self, tle):
        """
        Tell the mount to follow the supplied TLE.
        """

        print(f"Trigger to follow {tle}.")
        #self.mount.Follow_TLE(tle)

    def Move_AltAz(self, alt, az):
        self.mount.Goto_AltAz(alt, az)

    def Move_RaDec(self, ra, dec, j2000):
        if j2000:
            self.mount.Goto_RaDec_J2000(ra, dec)
        else:
            self.mount.Goto_RaDec_Apparent(ra, dec)

    def run(self):
        while self.thread_Active:
            status = self.mount.Status()
            self.status_Signal.emit(status)
            time.sleep(1)

    def stop(self):
        self.thread_Active = False
        self.wait()
