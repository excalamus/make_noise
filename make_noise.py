import os
import sys
import argparse
import subprocess
import atexit

from PySide2 import QtCore, QtWidgets, QtGui


PID = None
SOX = "sox.exe"

def resource_path(relative_path):
     if hasattr(sys, '_MEIPASS'):
         return os.path.join(sys._MEIPASS, relative_path)
     return os.path.join(os.path.abspath("."), relative_path)

class TrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent):

        global SOX

        super().__init__()

        self.parent = parent
        self.play_button = None
        self.sox = SOX
        self.subp = None

        self.is_playing = False

        self.setIcon(icon)

        self.init_widgets()

    def init_widgets(self):

        menu = QtWidgets.QMenu()

        self.menu_toggle = menu.addAction("Play")
        self.menu_toggle.triggered.connect(self.toggle_noise)
        self.menu_toggle.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))

        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(self.parent.quit)
        self.setContextMenu(menu)

        self.activated.connect(self.on_activated)


    def on_activated(self, reason):
        if reason == self.DoubleClick:
            self.toggle_noise()

    def toggle_noise(self):
        if self.is_playing:
            try:
                clean_up(pid=self.subp.pid)
                self.is_playing = False
                self.menu_toggle.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
                self.menu_toggle.setText("Play")
                icon = QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogYesButton)
                self.setIcon(icon)
            except:
                pass

        else:

            sox_path = 'bin\\'+self.sox
            print(sox_path, flush=True)
            args = [
                sox_path,
                '--no-show-progress',
                '-c 2',
                '--null',
                '-t waveaudio',
                'synth 3600 brownnoise',
                'band -n 1500 499',
                'tremolo 0.05 43',
                'reverb 19',
                'bass -11 ',
                'treble -1',
                'vol 14dB ',
                'fade q .01',
                'repeat 9999',
            ]

            the_call = ' '.join(args)
            self.subp = subprocess.Popen(the_call, shell=True)
            global PID
            PID = self.subp.pid
            self.is_playing = True
            self.menu_toggle.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_MediaStop))
            self.menu_toggle.setText("Stop")
            icon = QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogNoButton)
            self.setIcon(icon)


def clean_up(pid=None):
    if pid:
        try:
            os.system("taskkill /F /T /PID %i" % pid)
        except:
            pass
    else:
        try:
            global PID
            os.system("taskkill /F /T /PID %i" % PID)
        except:
            pass

    try:
        global SOX
        os.system("taskkill /F /T /IM %s" % SOX)
    except:
        pass

atexit.register(clean_up)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    icon = QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogYesButton)
    tray_icon = TrayIcon(icon, app)
    tray_icon.setToolTip('Make some noise!')
    tray_icon.show()

    app.aboutToQuit.connect(clean_up)
    sys.exit(app.exec_())
