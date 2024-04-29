# -*- coding: utf-8 -*-
import functools
import sys

# Form implementation generated from reading ui file 'dialog_win_about.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QDesktopServices, QUrl
from functools import partial


class Ui_Dialog(object):
    def setupUi(self, Dialog : QtWidgets.QDialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(690, 447)

        Dialog.resizeEvent = lambda e, ob = Dialog : self.resize_event(e, ob)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setWindowIcon(QIcon("Icons/general_logo.png"))
        Dialog.setMinimumSize(QtCore.QSize(690, 447))
        Dialog.setMaximumSize(QtCore.QSize(690, 447))
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(300, 370, 341, 32))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(90, 50, 161, 151))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Icons/general_logo150142.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(340, 50, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(340, 100, 391, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(340, 140, 391, 14))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(340, 170, 391, 21))
        self.label_5.setObjectName("label_5")
        self.commandLinkButton = QtWidgets.QCommandLinkButton(Dialog)
        self.commandLinkButton.setGeometry(QtCore.QRect(50, 360, 281, 48))
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.commandLinkButton.clicked.connect(self.open_web_site)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(90, 250, 531, 29))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(90, 240, 531, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(90, 280, 531, 29))
        self.label_8.setObjectName("label_8")
        self.label_4.raise_()
        self.buttonBox.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_5.raise_()
        self.commandLinkButton.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.label_8.raise_()

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def resize_event(self,e:QtCore.QEvent, ob: QtWidgets.QDialog):
        """
        This funciton is incharge when the dialog go to another monitors preserve the same size
        :param e:
        :param ob:
        :return:
        """
        ob.resize(690, 447)



    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "QNotePad V_1.0"))
        self.label_3.setText(_translate("Dialog", "Version : 1.0, April 2024"))
        self.label_4.setText(_translate("Dialog", "Made by : Cristian Felipe Espitia"))
        self.label_5.setText(_translate("Dialog", "Powered by: Fundacion AJ Eliza | Free software"))
        self.commandLinkButton.setText(_translate("Dialog", "&Fundacion AJ Eliza Website"))
        self.label_7.setText(_translate("Dialog", "Este software esta impulsado por la Fundacion AJ Eliza y Quantum Brey con el objetivo de"))
        self.label_6.setText(_translate("Dialog", "promover el uso de software libre y enseñar a través de este ideal"))
        self.label_8.setText(_translate("Dialog", "Licencia : Libre | Distribución y comercialización permitidos"))

    def display_dialog(self):
        dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(dialog)
        dialog.exec_()

    def open_web_site(self):
        """
        This funcion open the url if the link button is clicked
        :return:
        """
        url  = "https://fundacionajeliza2016.wixsite.com/inicio"
        QDesktopServices.openUrl(QUrl(url))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    window = Ui_Dialog()
    window.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())