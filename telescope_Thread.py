import datetime
import functools
import logging
import time
import sys

import tzlocal

from PyQt5 import QtCore

import LD_Planewave
import LD_PWI_Status

log = logging.getLogger(__name__)

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

        log.debug("Init thread defaults")

        self.thread_Active = False

        self.mount = LD_Planewave.LD_Planewave()

        self.waiting_List = []

    def Connect_Server(self, ip_Address, port):
        """
        Connect to the telescope HTTP server and tell the HTTP server to
        """

        log.debug(f"Connect to PWI4 HTTP server at {ip_Address}:{port}")

        response = self.mount.Connect_IP(ip_Address, port)
        self.thread_Active = True

        return response

    def Connect_Mount(self):
        """
        connect to the physical hardware.
        """

        log.debug("Connect PWI4 to telescope mount")
        return self.mount.Connect()

    def Enable_Axis(self, axis):
        """
        Enable the set telescope axis.
        """
        return self.mount.Enable(axis)

    def Disable_Axis(self, axis):
        """
        Disable the set telescope axis
        """
        return self.mount.Disable(axis)

    def Disconnect(self):
        """
        Disconnect from the telescope
        """

        log.debug("Disconnect PWI4 from telescope mount")
        return self.mount.Disconnect()

    def Add_Waiting_TLE(self, tle, start, stop):
        """
        Add a TLE to the waiting list of TLEs to track. Use a QTimer to fire
        the TLE tracking function at (roughly) "start".
        "stop" is just used for displaying the pass stop time to the user.
        """

        log.info(f"Add {tle.name.rstrip()} to waiting list. Trigger at {start}")

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
            log.debug(f"start {start} added at {now}, which is {delta_ms} away")
            timer.start(delta_ms)

            # Add the info to a list to keep track of all the timers.
            # Keep the list sorted for clarity
            self.waiting_List.append([tle, start, stop, timer])
            self.waiting_List.sort(key=lambda x: x[1])

            # Emit the list so the GUI can update.
            self.waiting_Signal.emit(self.waiting_List)
        elif (now < stop):
            log.warning("Error? pass already started. tracking remainder of it")
            self.Follow_TLE(tle)
        else:
            log.warning("Error, pass has already happened.")

    def Remove_Waiting_TLE(self, index):
        """
        Remove a TLE from the waiting list (maybe it was added by accident?)
        and stop the follow command from being fired.
        """

        log.info(f"Remove element {index} from the TLE waiting list. Was {self.waiting_List[index]}")

        # Stop the timer from the selected row
        self.waiting_List[index][3].stop()
        # Remove selected row
        self.waiting_List.pop(index)

        # Send a signal so the GUI updates.
        self.waiting_Signal.emit(self.waiting_List)

    def Triggered_Follow_TLE(self, tle):
        """
        If the follow tle was triggered by a QTimer, it must be
        the first one in the waiting list? If so we can remove it, update the
        GUI and trigger the actual follow command
        """

        log.info(f"TLE track trigger received, follow {tle.name}")
        log.info(f"Remove TLE from list {self.waiting_List[0][0].name}")

        self.waiting_List.pop(0)
        self.waiting_Signal.emit(self.waiting_List)

        self.Follow_TLE(tle)

    def Follow_TLE(self, tle):
        """
        Tell the mount to follow the supplied TLE.
        """

        log.debug(f"Follow\n{tle}")
        return self.mount.Follow_TLE(tle)

    def Move_AltAz(self, alt, az):
        log.debug(f"Go to alt/az: {alt}, {az}")
        return self.mount.Goto_AltAz(alt, az)

    def Move_RaDec(self, ra, dec, j2000):
        log.debug(f"Go to ra/dec {ra}, {dec}. J2000?{j2000}")
        if j2000:
            return self.mount.Goto_RaDec_J2000(ra, dec)
        else:
            return self.mount.Goto_RaDec_Apparent(ra, dec)

    def Mount_Stop(self):
        log.debug("Stop mount")
        return self.mount.Stop()

    def Mount_Park(self, here):
        log.debug("Park mount. Here?{here}")
        if here:
            return self.mount.Park_Here()
        else:
            return self.mount.Park()

    def Mount_Home(self):
        log.debug("Home mount")
        return self.mount.Home()

    def Mount_Tracking(self, on):
        if on:
            log.debug("Mount tracking on")
            return self.mount.Tracking_On()
        else:
            log.debug("Mount tracking off")
            return self.mount.Tracking_Off()

    def Raw_Cmd(self, cmd):
        return self.mount.Raw_Command(cmd)

    def run(self):
        log.debug("Start mount status reports")
        while self.thread_Active:
            status = self.mount.Status()
            self.status_Signal.emit(status)
            time.sleep(1)

    def stop(self):
        log.debug("Stop mount status reports")
        self.thread_Active = False
        self.wait()
