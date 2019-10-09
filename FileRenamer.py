from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from qtpy import QtCore
import os
import re

path = ''

app = QApplication([])
dlg = loadUi('ui.ui')

def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


def browseImg():
    global path
    path = QFileDialog.getExistingDirectory(dlg, "Select Directory")
    print(path)


def infoDialogue():
    infoBox = QMessageBox()
    infoBox.setIcon(QMessageBox.Information)
    infoBox.setText(str(len(os.listdir(path))) + " items successfully renamed.")
    infoBox.setWindowTitle("Success")
    infoBox.setStandardButtons(QMessageBox.Ok)
    infoBox.setEscapeButton(QMessageBox.Close)
    infoBox.exec()


def rename():
    global path
    if path != '' and dlg.prefix.text() != '' and dlg.suffix.text() != '' and dlg.counter.text() != '':
        i = int(dlg.counter.text())
        for filename in sorted_aphanumeric(os.listdir(path)):
            print(filename)
            dst = dlg.prefix.text() + str(i) + dlg.suffix.text()
            src = path + '/' + filename
            dst = path + '/' + dst
            os.rename(src, dst)
            i += 1
        infoDialogue()
        dlg.prefix.setText('')
        dlg.counter.setText('')
        dlg.suffix.setText('')
        path = ''
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText('Fill all necessary details !')
        msg.setWindowTitle("Error")
        msg.exec_()


label = dlg.image
pixmap = QPixmap('testimg.jpg')
pixmap = pixmap.scaled(pixmap.width() - 50, pixmap.height() / 1.7)
label.setPixmap(pixmap)
label.resize(pixmap.width(), pixmap.height())
dlg.resize(pixmap.width(), pixmap.height())

dlg.browse.clicked.connect(browseImg)
dlg.rename.clicked.connect(rename)

dlg.setAttribute(QtCore.Qt.WA_DeleteOnClose)
dlg.setWindowFlags(dlg.windowFlags() |
                   QtCore.Qt.WindowSystemMenuHint |
                   QtCore.Qt.WindowMinimizeButtonHint)

dlg.show()
app.exec()
