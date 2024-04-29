import sys
from PyQt5.QtGui import QClipboard
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets


class ClipBoard:

    """
    This class is incharge to verify is there is somethin on the clipBoard and additoinally  clear the clip_board if needed
    """

    def __init__(self):
        super().__init__()
        self.clip_board = QApplication.clipboard()
        self.data: QClipboard = None

    @property
    def check_clip_board(self):
        """
        This function will check if the clipboard has a text
        :return:
        """
        self.clip_board = QApplication.clipboard()
        self.data = self.clip_board.mimeData()
        self.image = self.clip_board.image()

        if self.data.hasText():
            return True
        elif self.data.hasImage():
            return False

    def get_clip_board_content(self):
        return self.data.text()

    def clear_clip_board(self):
        self.clip_board.clear()
