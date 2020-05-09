# This Python file uses the following encoding: utf-8
import os
import sys
import configparser

from PySide2 import QtCore
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject

from serial import Serial         # pip3 install pyserial
from serial.tools import list_ports


class QmlSer(QObject):
    def __init__(self, context, parent=None):
        super().__init__(parent)
        self.win = parent
        self.ctx = context

        self.cmbPort = self.win.findChild(QObject, 'cmbPort')
        self.btnOpen = self.win.findChild(QObject, 'btnOpen')
        self.lblTip = self.win.findChild(QObject, 'lblTip')


        portsStr = []
        for port, desc, hwid in list_ports.comports():
            portsStr.append(port)

        self.cmbPort.setProperty('model', portsStr)

        self.ser = Serial()

        self.initSetting()

    def initSetting(self):
        if not os.path.exists('setting.ini'):
            open('setting.ini', 'w')
        self.conf = configparser.ConfigParser()
        self.conf.read('setting.ini')

        if not self.conf.has_section('serial'):
            self.conf.add_section('serial')
            self.conf.set('serial', 'port',     'COM0')
            self.conf.set('serial', 'baudrate', '115200')

        self.cmbPort.setProperty('currentIndex', self.cmbPort.find(self.conf.get('serial', 'port'), QtCore.Qt.MatchExactly))

    @QtCore.Slot()
    def on_btnOpen_clicked(self):
        if not self.ser.is_open:
            try:
                 self.ser= Serial(self.cmbPort.property('currentText'), 115200)
            except Exception as e:
                print(e)
                self.lblTip.setProperty("text", self.tr('打开串口出错:\n %s' %(e)))
            else:
                self.btnOpen.setProperty('text', self.tr('关闭串口'))
        else:
            self.ser.close()
            self.btnOpen.setProperty('text', self.tr('打开串口'))

    @QtCore.Slot()
    def on_closed(self):
        self.ser.close()
        self.conf.set('serial', 'port',     self.cmbPort.property('currentText'))
        self.conf.set('serial', 'baudrate', "115200")
        self.conf.write(open('setting.ini', 'w'))

    @QtCore.Slot()
    def on_btnRead_clicked(self):
        if self.ser.is_open:
            if self.ser.in_waiting > 0:
                bytes = self.ser.read(self.ser.in_waiting)
                print(bytes.decode('latin'))


if __name__ == '__main__':
    app = QGuiApplication(sys.argv)

    qml = QQmlApplicationEngine('main.qml')

    qml.rootContext().setContextProperty('Ser', QmlSer(qml.rootContext(), qml.rootObjects()[0]))

    sys.exit(app.exec_())
