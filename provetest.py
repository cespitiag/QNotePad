import sys

import setuptools
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QApplication, QTextEdit
from PyQt5.QtPrintSupport import  QPrintPreviewDialog, QPrinter
from PyQt5.QtCore import QSizeF
from PyQt5.QtGui import  QPageSize

class MainWidget(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)

        self.text_edit :QTextEdit = QTextEdit(self)
        self.preview_button= QPushButton(self, text ="&Preview Button")
        self.printer: QPrinter = QPrinter()

        self.preview_button.clicked.connect(self.preview_clicked)

        self.text_edit.setGeometry(10,10, 100,30)
        self.preview_button.setGeometry(10,50, 100,30)

    def preview_clicked(self):
        dialog_privew = QPrintPreviewDialog()
        dialog_privew.paintRequested.connect(self.display_paint_view)
        dialog_privew.exec_()

    def display_paint_view(self,printer):
        self.printer : QPrinter= printer
        self.printer.setDocName(f"{self.windowTitle()} - ")
        self.printer.setPageSize(QPageSize(QPageSize.Letter))
        document = self.text_edit.document()
        document.setPageSize(QSizeF(1,1))
        document.print_(self.printer)







if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWidget()
    window.show()
    sys.exit(app.exec_())