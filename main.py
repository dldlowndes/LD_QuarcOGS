"""
Basic GUI example. A button that makes a number count upwards (or stop
counting upwards)
"""

# pylint: disable=C0103
# pylint: disable=R0902

import sys

from PyQt5 import QtWidgets, QtCore, QtGui
import settings_gui
import worker_Thread

class MyWindow(QtWidgets.QMainWindow):
    """
    Window for the UI for the Polsnap program.
    """
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = settings_gui.Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.Init_Defaults()
        self.Init_Threads()
        self.Init_Connections()
        
    def Init_Defaults(self):
        pass

    def Init_Threads(self):
        self.worker_Thread = worker_Thread.worker_Thread(1.5)
        self.worker_Thread.output_Signal.connect(self.On_Return_Signal)
        self.worker_Thread.start()

    def Init_Connections(self):
        self.ui.button_Go.clicked.connect(self.On_Run_Button)

    def On_Run_Button(self):
        print(f"Pressed button")
        if self.worker_Thread.running:
            self.worker_Thread.running = False
        else:
            self.worker_Thread.running = True

    def On_Return_Signal(self, value):
        self.ui.display_Value.setText(f"{value:.2f}")
        

app = QtWidgets.QApplication([])

application = MyWindow()

application.show()

sys.exit(app.exec())
