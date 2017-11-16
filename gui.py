# -*- coding: utf-8 -*-

from sys import argv

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QDialog

from scrape import get_translation


class search_thread(QThread):
    parse_triggered = pyqtSignal()
    done = pyqtSignal(list)

    def __init__(self):
        QThread.__init__(self)
        self.jp_text = None

    def __del__(self):
        self.wait()

    def set_jp_text(self, jp_text):
        self.jp_text = jp_text

    def run(self):
        data = get_translation(self.jp_text)
        self.done.emit(data)


class Ui_Dialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.worker = search_thread()
        self.setupUi()
        self.set_connections()

    def setupUi(self):
        self.setObjectName("self")
        self.resize(842, 443)
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 821, 431))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.jp_text = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.jp_text.setObjectName("jp_text")
        self.horizontalLayout.addWidget(self.jp_text)
        self.search_btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.search_btn.setObjectName("search_btn")
        self.horizontalLayout.addWidget(self.search_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.result = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.result.sizePolicy().hasHeightForWidth())
        self.result.setSizePolicy(sizePolicy)
        self.result.setReadOnly(True)
        self.result.setTabStopWidth(81)
        self.result.setObjectName("result")
        self.verticalLayout.addWidget(self.result)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Jisho"))
        self.search_btn.setText(_translate("self", "Search"))
        self.result.setDocumentTitle(_translate("self", "Translation"))
        self.result.setPlaceholderText(_translate("self", "Translation"))

    def set_connections(self):
        self.jp_text.returnPressed.connect(self.search)
        self.jp_text.setFont(QFont('Arial', 16))
        self.search_btn.clicked.connect(self.search)
        self.result.setFont(QFont('Arial', 16))

    def search(self):
        self.jp_text.setDisabled(True)
        self.search_btn.setDisabled(True)
        jp_text = self.jp_text.text()
        self.worker.set_jp_text(jp_text)
        self.worker.done.connect(self.done)
        self.worker.start()

    def done(self, data):
        s = str()
        for part in data:
            s += "(%s) %s : %s = %s\n\n" % (
            part[2], part[0], part[1], part[3][0])

        self.result.setPlainText(s)
        self.jp_text.setDisabled(False)
        self.search_btn.setDisabled(False)


if __name__ == '__main__':
    app = QApplication(argv)

    aw = Ui_Dialog()
    aw.show()
    app.exec_()
