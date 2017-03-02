# -*- coding: utf-8 -*-

"""
Main executable for ING2YNAB csv converter.

@author: Luc van Dort
"""


import sys
from PyQt5.QtWidgets import QAction, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.main_widget = MainWidget(self)
        _widget = QWidget()
        _layout = QVBoxLayout(_widget)
        _layout.addWidget(self.main_widget)
        self.setCentralWidget(_widget)

        self.initUI()

    def initUI(self):
        self.selectInputfile = QAction(QIcon('open.png'), 'Select input file', self)
        self.selectInputfile.triggered.connect(self.inputfileDialog)
        self.selectOutputfolder = QAction(QIcon('open.png'), 'Select output folder', self)
        self.selectOutputfolder.triggered.connect(self.outputfolderDialog)

        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&File')
        self.fileMenu.addAction(self.selectInputfile)
        self.fileMenu.addAction(self.selectOutputfolder)

        self.resize(500, 100)
        self.setWindowTitle('ING2YNAB')
        self.show()
        self.center()

    def inputfileDialog(self):
        filename = QFileDialog.getOpenFileName(self, 'Select input file')
        self.main_widget.inputfile.setText(filename[0])  

    def outputfolderDialog(self):
        foldername = QFileDialog.getExistingDirectory(self, 'Select output folder')
        self.main_widget.outputfolder.setText(foldername)  

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class MainWidget(QWidget):

    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)
        self.__controls()
        self.__layout()

    def __controls(self):
        
        self.convertButton = QPushButton("Convert")

        self.quitButton = QPushButton("Quit")
        self.quitButton.clicked.connect(QCoreApplication.instance().quit)

        self.lbl_inputfile = QLabel('Input file')
        self.lbl_outputfolder = QLabel('Output folder')

        self.inputfile = QLineEdit()
        self.outputfolder = QLineEdit()

    def __layout(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.lbl_inputfile, 1, 0)
        self.grid.addWidget(self.inputfile, 1, 1)

        self.grid.addWidget(self.lbl_outputfolder, 2, 0)
        self.grid.addWidget(self.outputfolder, 2, 1)

        self.buttonbox = QHBoxLayout()
        self.buttonbox.addStretch(1)
        self.buttonbox.addWidget(self.convertButton)
        self.buttonbox.addWidget(self.quitButton)

        self.layout = QVBoxLayout()
        self.layout.addStretch(1)
        self.layout.addLayout(self.grid)
        self.layout.addLayout(self.buttonbox)

        self.setLayout(self.layout)






def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()

if __name__ == '__main__':
    
    sys.exit(main())
