import time

from PyQt5 import QtCore


class worker_Thread(QtCore.QThread):
    """
    Do some work. Emit signals when results are ready
    """

    # Signals to carry the collected data out of the thread.
    # Separate so mode can
    # be easily toggled on/off.
    output_Signal = QtCore.pyqtSignal(float)

    def __init__(self, init_Value):
        QtCore.QThread.__init__(self)

        # Flags.
        # Practically the thread will probably remain active whilever
        # the program is running.
        self.thread_Active = True

        self.running = False
        
        self.value = init_Value

    def run(self):
        while self.thread_Active:
            if self.running:            
                self.value += 1
                print(f"value: {self.value}")
                self.output_Signal.emit(self.value)
            else:
                pass
            
            time.sleep(1)


    def stop(self):
        self.thread_Active = False
        self.wait()
