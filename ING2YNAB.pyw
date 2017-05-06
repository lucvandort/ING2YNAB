# -*- coding: utf-8 -*-

"""
Main executable for ING2YNAB csv converter.

@author: Luc van Dort
"""

import sys, os
import pandas as pd
from PyQt5.QtWidgets import QAction, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication

EXPORT_COLUMNS = [
    "Date",
    "Payee",
    "Category",
    "Memo",
    "Outflow",
    "Inflow"
]

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

        self.resize(800, 100)
        self.setWindowTitle('ING2YNAB')
        self.show()
        self.center()

    def inputfileDialog(self):
        filename = QFileDialog.getOpenFileName(self, 'Select input file')
        self.main_widget.inputfile.setText(filename[0])
        path, file = os.path.split(filename[0])  
        self.main_widget.outputfolder.setText(os.path.join(path,"YNAB"))
        self.main_widget.outputfile.setText("YNAB_{}".format(file))

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
        self.convertButton.clicked.connect(self.convertAction)

        self.quitButton = QPushButton("Quit")
        self.quitButton.clicked.connect(QCoreApplication.instance().quit)

        self.lbl_inputfile = QLabel('Input file:')
        self.lbl_outputfolder = QLabel('Output folder:')
        self.lbl_outputfile = QLabel('Output file:')

        self.inputfile = QLineEdit()
        self.outputfolder = QLineEdit()
        self.outputfile = QLineEdit()

    def __layout(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.lbl_inputfile, 1, 0)
        self.grid.addWidget(self.inputfile, 1, 1)

        self.grid.addWidget(self.lbl_outputfolder, 2, 0)
        self.grid.addWidget(self.outputfolder, 2, 1)

        self.grid.addWidget(self.lbl_outputfile, 3, 0)
        self.grid.addWidget(self.outputfile, 3, 1)

        self.buttonbox = QHBoxLayout()
        self.buttonbox.addStretch(1)
        self.buttonbox.addWidget(self.convertButton)
        self.buttonbox.addWidget(self.quitButton)

        self.layout = QVBoxLayout()
        self.layout.addStretch(1)
        self.layout.addLayout(self.grid)
        self.layout.addLayout(self.buttonbox)

        self.setLayout(self.layout)

    def convertAction(self):
        converter = Converter(inputfile=self.inputfile.text())
        converter.convert()
        converter.write_outputfile(self.outputfolder.text(), self.outputfile.text())

class Converter():

    def __init__(self, inputfile):
        self.inputdata = pd.read_csv(inputfile, parse_dates = [0])
        self.outputdata = pd.DataFrame(index=self.inputdata.index, columns=EXPORT_COLUMNS, data=None)

    def convert(self):
        self.outputdata['Date'] = self.inputdata['Datum']
        self.outputdata['Payee'] = self.inputdata['Naam / Omschrijving']
        self.outputdata['Memo'] = self.inputdata['Mededelingen']
        self.outputdata['Outflow'] = self.inputdata[self.inputdata['Af Bij'] == 'Af']['Bedrag (EUR)']
        self.outputdata['Inflow'] = self.inputdata[self.inputdata['Af Bij'] == 'Bij']['Bedrag (EUR)']
        self.outputdata.fillna('', inplace=True)

    def write_outputfile(self, outputfolder, outputfile):
        os.makedirs(outputfolder, exist_ok=True)
        self.outputdata.to_csv(os.path.join(outputfolder, outputfile))

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()

if __name__ == '__main__':
    sys.exit(main())
