from typing import Tuple, Optional
import copy
from NotePad import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QTabWidget, QSizePolicy, QWidget,
                             QApplication, QMainWindow, QDialog,
                             QFileDialog, QMessageBox, QPlainTextEdit, QUndoStack, QUndoCommand, QAction)
from PyQt5.QtGui import QIcon, QFont, QTextCursor, QPageSize
from PyQt5 import QtPrintSupport
from PyQt5.QtPrintSupport import  QPrintDialog, QPrinter, QPageSetupDialog, QPrintPreviewDialog, QPrintPreviewWidget
from PyQt5.QtCore import Qt, pyqtSignal, QSizeF

import os
import System_info
from Clip_board import ClipBoard
from dialog_win_about import Ui_Dialog


class MainWindowApp(QMainWindow):
    """
    This Widge creates a tab with a QPlainTextEdit widget inside each tab
    :func __init__()
    :param func openFile()
    :param func saveFileAs ()
    :param func loadFileToOpen()
    :param list files : temporal storage while the application is working
    :param func None
    """
    def __init__(self) -> object:
        super().__init__()

        # Creating a user Interface object      
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.files = [] # Temporal
        self.identifier = 0
        self.rows, self.colums = 1,1

        #Create additional objects
        self.clip_board = ClipBoard()

        # The next variable are create Once the user change the tab this variable will change also
        self.current_plain_text_widget = self.ui.tabWidget.plainTextEditWidget # Initialize on the tab 1
        self.document : QPlainTextEdit.document() = self.current_plain_text_widget.document()
        self.current_plain_text_widget.setFocus(True)
        self.current_tab_info: TabsInfo = self.ui.tabWidget.tabsInfo[0] # This variable save the objec that contains additional properties

        # Documentation Properties
        self.printer = QPrinter()
        self.printer_name = None
        self.page_size = None
        self.page_orientation = None
        self.page_margins = None

        # Connecting Signals and Events
        self.ui.tabWidget.s_update_plain_text_edit.connect(self.update_plain_text_widget)
        self.ui.tabWidget.s_is_the_tab_saved.connect(lambda a : self.document_status_receive_signal_to_close(a))
        self.ui.menuEdit.aboutToShow.connect(self.menu_file_clicked)
        self.ui.actionNew_Tab.triggered.connect(self.addTab)
        self.ui.actionClose_Tab.triggered.connect(self.close_tab)
        self.ui.actionNew_Window.triggered.connect(self.NewWindow)
        self.ui.actionOpen.triggered.connect(self.openFile)
        self.ui.actionSave_all_2.triggered.connect(self.save_all)
        self.ui.actionSave_as.triggered.connect(self.saveFileAs)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionClose_Window.triggered.connect(self.closeWindow)
        self.ui.actionPage_preview.triggered.connect(self.prin_preview)
        self.ui.actionPrint.triggered.connect(self.print_document)
        self.ui.actionEnableTrackMode.triggered.connect(self.set_enable_track)
        self.ui.actionZoom_in.triggered.connect(self.zoom_in_tab)
        self.ui.actionZoom_out.triggered.connect(self.zoom_out_tab)
        self.ui.actionPaste.triggered.connect(self.paste)
        self.ui.actionCopy.triggered.connect(self.copy)
        self.ui.actionCut.triggered.connect(self.cut)
        self.ui.actionDelete_2.triggered.connect(self.delete_2)
        self.ui.actionTime_Date.triggered.connect(self.insert_date_today)
        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionRedo.triggered.connect(self.redo)
        self.ui.actionStatus_bar.triggered.connect(self.hide_show_status_bar)
        self.ui.actionAbout.triggered.connect(self.display_about_window)
        self.current_plain_text_widget.copyAvailable.connect(lambda e: self.selection_enable(e))

        self.current_plain_text_widget.textChanged.connect(self.text_is_being_editing)
        self.current_plain_text_widget.cursorPositionChanged.connect(self.cursor_position_changed)
        self.current_plain_text_widget.undoAvailable.connect(self.undo_available)
        self.current_plain_text_widget.redoAvailable.connect(self.redo_available)

        # Update the rows and colums visualizationa and then connect the signal to continue editing
        self.ui.statusLabel_1.setText(f"Column : {self.colums} Line: {self.rows}")
        self.ui.statusLabel_2.setText(f"Total Characters: {len(self.current_plain_text_widget.toPlainText())}")
        self.ui.statusLabel_3.setText(f"Zoom: {self.current_tab_info.zoom} %")

        # Define the operative system
        self.ui.statusLabel_4.setText(f"OS: {str(System_info.OS_SYSTEM)}")
        # Define the codification style
        self.ui.statusLabel_5.setText("UTF-8")

        #Additional widgets
        self.auto_check_box : QtWidgets.QCheckBox = QtWidgets.QCheckBox("Autonumbering")
        self.auto_check_box.setIcon(QIcon("Icons/page_numbering.png"))
        self.auto_check_box.setChecked(False)
        self.auto_check_box.setToolTip("Autonumberate your pages\n"
                                       "\n"
                                       "Clicked this checkbox will autoenumerate the pages on your document")
        self.auto_check_box.clicked.connect(self.auto_num_checked)


        self.preview_page_dialog : QPrintPreviewDialog = None

    def openFile(self):
        """
        This Function open the files and open a Dialog box
        """
        options = QFileDialog.Options()  # The options on the QFileDialog to be modified
        # options |= QFileDialog.DontUseNativeDialog # Utilizing bit operations to say the program don't use native inter

        # This line return the value in a tuple (Adreess, action)
        filePath, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);Text Files (*.txt)",
                                                  options=options)

        if not filePath:
            return

        content = self.loadFileToOpen(filePath)

        # If the file is open this code will verify if the file exist
        index_result = self.ui.tabWidget.adddres_in_tab_exist(filePath)

        if index_result != -1 and index_result != self.ui.tabWidget.currentIndex():
            # If it is already open it will set the vizualization to the current file
            self.ui.tabWidget.tab_in_vizualize = index_result
            self.ui.tabWidget.setCurrentIndex(index_result)

        elif self.ui.tabWidget.currentIndex() == index_result:
            # This is in the case that
            pass

        else:
            # if it is not open it will charge the file to the notepath
            self.ui.tabWidget.addTab(name=self.getNameFromPath(filePath), path=filePath)  # Add a tab with a name

            # Change the current tab to the position Suggested
            self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)

            # Return the current widget ont he specific tab the customer is seeing
            tab = self.currentWidgetInTab()
            tab.clear()  # If there is something in the tab, it would clear the complete tab
            tab.insertPlainText(content)  # Give the content to the widget PlainTextEdit

        self.save_document_status = True


    def saveFileAs(self):
        """
        This Funciont will open a DialogBox to save the projects
        this funcion consist in rewrite and create files if it is necessary
        """
        index: int | None = self.ui.tabWidget.currentIndex()  # Obtain the current_index on the tab the user is seeing
        name: str | None = self.ui.tabWidget.tabText(index)  # Obtain the current_index on the default name

        # Example options |= QFileDialog.DontUseNativeDialog
        # Example options |= QFileDialog.DontConfirmOverwrite
        # Example options |= QFileDialog.ShowDirsOnly
        options = QFileDialog.Options()  # Getting the options and this object is ready to be modified with

        # this notation means that filepath could be a tuple with string or None
        filePath, _ = QFileDialog.getSaveFileName(self, "Save as", f"{name}", "Text file (*.txt)")
        try:
            if filePath:  # Verify if the path exist

                with open(filePath, "w", encoding="utf-8") as txt:
                    tab = self.currentWidgetInTab()
                    text = tab.toPlainText()
                    txt.write(text)

                # This function return the name this function is placed on that class
                newName = self.getNameFromPath(filePath) if self.getNameFromPath(filePath) != "" else name
                self.ui.tabWidget.setTabText(index, newName)

                index_tab = self.ui.tabWidget.adddres_in_tab_exist(filePath)
                if index_tab == -1:
                    self.ui.tabWidget.tabsInfo[index].path = filePath # Add the new path to the indicator
                    self.ui.tabWidget.tabsInfo[index].name = self.getNameFromPath(filePath)
                else:
                    # If the current_index exist do not do anything
                    pass

                self.save_document_status = True # The document has been saved



        except Exception as e:
            errorWindow = WindowsInfo("Error", e,0)
            errorWindow.exec_()

    def save(self, index : int = None):
        """
        This function compromise if the file exist in a specific path in the case that the file does not exist
        It will display a save as function in order to host the file on the path
        """

        def write (path):
            # This function write the changes
            with open(path, 'w', encoding= 'utf-8') as txt:
                widget = self.currentWidgetInTab()
                text = widget.toPlainText()
                txt.write(text)


        # Verify the current current_index
        current_index = index if index else  self.ui.tabWidget.currentIndex()
        obj_tab = self.ui.tabWidget.tabsInfo[current_index]

        if current_index in self.ui.tabWidget.tabsInfo and self.ui.tabWidget.tabsInfo[current_index].path != None:
            write(obj_tab.path)
            self.save_document_status = True
        else:
            self.saveFileAs()

    def save_all(self):
        for tab in self.ui.tabWidget.tabsInfo:
            self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.currentIndex())
            self.save(tab)

        # for tab in self.ui.tabWidget.tabsInfo:
        #     print(tab)
        #     self.save(tab)


    def closeWindow(self,a):
        self.close()

    @staticmethod
    def loadFileToOpen(file: object) -> str:
        """
        Upload txt files to read and open it in the application
        :type actions : This refer to verify if open or save
        :return content : return the text
        """
        content = ""
        with open(file, 'r', encoding="utf-8") as txt:
            content = txt.read()

        return content

    def addTab(self):
        """
        This Function will add a tab reusing the tabWidget.addtab() method
        """
        assert isinstance(self.ui.tabWidget.addTab, object)
        self.ui.tabWidget.addTab()

    def close_tab(self, event):

        """
        When you select close tab it will catch the current tab current_index and then It will close it
        :param event : is not use for this case
        """

        if self.save_document_status:
            self.__deleting_tab()
        else:
            self.ask_to_save(self.save, self.__deleting_tab)

    def __deleting_tab(self):
        """
        This is a private function due to
        :return:
        """

        self.save_document_status = True
        index = self.ui.tabWidget.currentIndex()
        self.current_plain_text_widget.textChanged.disconnect
        self.ui.tabWidget._tab_close_request(index)
    def NewWindow(self):
        """
        Create a New MainApp with the same functionalities
        """
        MainWindow = MainWindowApp()
        MainWindow.show()

    def zoom_in_tab(self):

        if int (self.current_tab_info.zoom) < 800:
            increse = 10
            self.current_plain_text_widget.zoomIn(range = 1) # Verify Documentation
            self.current_tab_info.zoom += increse
            self.update_zoom_label()



    def zoom_out_tab(self):

        if int(self.current_tab_info.zoom) > 10: # Dont exced the limit
            increase = 10
            self.current_plain_text_widget.zoomOut(range = 1) # Verify Documentation
            self.current_tab_info.zoom -= increase
            self.update_zoom_label()
        else:
            pass

    def currentWidgetInTab(self) -> QWidget:
        """
        return the current_index on the current Tab
        :return: QPlainTextEdit Object
        """
        index: int = self.ui.tabWidget.currentIndex()
        widget: QWidget | None = self.ui.tabWidget.widget(index)
        return widget

    def getCurrentTab(self):
        index = self.ui.tabWidget.currentIndex()
        name = self.ui.tabWidget.tabBar().tabText(index)
        return index, name


    def getNameFromPath(self, filePath) -> str:
        """
        :param filePath:
        :return: str name
        """
        name = filePath.split('/')[-1]
        name = name.split(".txt")[0]
        return name


    def text_is_being_editing(self):
        """
        This function is incharge of change the comlums and rows on the labels and change the save status to false
        due to the document has been edited
        :return:
        """
        text = self.current_plain_text_widget.toPlainText()
        total = len(text)

        if total == 0:
            self.rows, self.colums, total = 1, 1, 0
            self.update_colum_rows()
            self.save_document_status = True

        else:
            self.update_colum_rows()
            self.ui.tabWidget.tab_track[1] = self.ui.tabWidget.currentIndex() # Variabe should be public to use here
            self.ui.tabWidget.last_index_clicked = self.ui.tabWidget.currentIndex() # The variable shoud be public
            self.save_document_status = False

        self.ui.statusLabel_2.setText(f"Total Characters: {total}")
    def update_zoom_label(self):
        self.ui.statusLabel_3.setText("Zoom: "+str(self.current_tab_info.zoom)+ " %")

    def update_plain_text_widget(self, tab_info: TabsInfo):
        """
        Disconnect the signal to the old plain text edit, and connect it to the current signal
        :param plain_text:
        :return:
        """

        try:
            
            self.current_tab_info = tab_info
            self.disconnect_signals()
            self.current_plain_text_widget = tab_info.plain_text_widget
            self.connecting_signals()
            self.update_widgets_features()
            # Connect the cursor changed

        except AttributeError as e: # When it starts it does not have any element into the dictionary.
            raise e

    def cursor_position_changed(self):
        """
        This function will update the rows and the columns
        :return:
        """
        self.rows = self.current_plain_text_widget.textCursor().blockNumber() + 1
        self.colums = self.current_plain_text_widget.textCursor().columnNumber() +1
        self.update_colum_rows()

    def update_colum_rows(self):
        self.colums = self.current_plain_text_widget.textCursor().columnNumber() + 1
        self.rows = self.current_plain_text_widget.textCursor().blockNumber() + 1
        self.ui.statusLabel_1.setText(f"Column : {self.colums} Line: {self.rows}")


    def set_enable_track(self):

        value = self.ui.actionEnableTrackMode.isChecked()
        self.ui.tabWidget.set_enable_tab_track(value)

    def hide_show_status_bar(self):
        e = not self.ui.actionStatus_bar.isChecked()
        self.ui.statusbar.setHidden(e)

    def disconnect_signals(self):
        """
        Disconnect masive signals
        :return:
        """
        self.current_plain_text_widget.textChanged.disconnect()
        self.current_plain_text_widget.cursorPositionChanged.disconnect()
        self.current_plain_text_widget.copyAvailable.disconnect()
        self.current_plain_text_widget.undoAvailable.disconnect(self.undo_available)

    def connecting_signals(self):
        """
        Connecting masive signals
        :return:
        """
        self.current_plain_text_widget.cursorPositionChanged.connect(self.cursor_position_changed)
        self.current_plain_text_widget.textChanged.connect(self.text_is_being_editing)
        self.current_plain_text_widget.copyAvailable.connect(self.selection_enable)
        self.current_plain_text_widget.undoAvailable.connect(self.undo_available)

    def update_widgets_features(self):
        """
        Update the current widgets to reestablish his properties
        :return:
        """
        self.text_is_being_editing()
        self.cursor_position_changed()
        self.update_zoom_label()
        self.is_undo_available()


    @property
    def save_document_status(self) -> bool:
        return self.current_tab_info.save

    @save_document_status.setter
    def save_document_status(self, is_saved: bool):
        self.current_tab_info.save = is_saved

    def document_status_receive_signal_to_close(self, e : bool) -> bool:
        """
        This function incharge to receive the signal and validate if the page is optim to close
        :param e:
        :return:
        """
        self.save_document_status = e
        self.close_tab(e) # the funcion is receiving the same signal

    def ask_to_save(self, save_func : object = None, del_func: object = None):

        """
        This Fucnion is creating a diaglog window to ask the custoemr if want to save or not the content
        :param save_func:
        :param del_func:
        :return:
        """
        index = self.ui.tabWidget.currentIndex()

        reply = QMessageBox.question(self,
                                     "Save the changes",
                                     f"Do you want to save the changes for {self.ui.tabWidget.tabsInfo[index].name}?",
                                     QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Save)

        if reply == QMessageBox.Save:
            save_func()
        elif reply == QMessageBox.Discard:
            del_func()
        else:
            pass

    def auto_num_checked(self):
        value = self.auto_check_box.checkState()
        self.auto_check_box.setChecked(value)


    def prin_preview(self):
        """
        This funciton create a window that allows to the customer customize his page size
        :return: QPrinter
        """
        self.preview_page_dialog = QPrintPreviewDialog()
        self.preview_page_dialog.setWindowIcon(QIcon("Icons/Main_logo.png"))
        self.preview_page_dialog.paintRequested.connect(self.prepare_the_document_to_visualize)
        self.preview_page_dialog.exec_()


    def prepare_the_document_to_visualize(self,printer: QPrinter):
        self.printer = printer
        self.printer.setDocName(f"{self.windowTitle()} - " + str(self.current_tab_info.name))
        self.document = self.current_plain_text_widget.document()
        self.document.print_(self.printer)


    def print_document(self):

        self.printer = QPrinter()

        dialog_printer = QPrintDialog(self.printer)
        if dialog_printer.exec_():

            self.printer.setDocName(f"{self.windowTitle()} - " + str(self.current_tab_info.name))
            self.document = self.current_plain_text_widget.document()
            self.document.print_(self.printer)





    def menu_file_clicked(self):
        """
        This function receive the signal to enable or desable the option on the menu
        :param event: event is receiving the signale that comes from it is avalable to copy or not
        :return:
        """
        self.current_tab_info.paste = True if self.clip_board.check_clip_board else False
        self.ui.actionPaste.setEnabled(self.current_tab_info.paste)
        self.ui.actionCopy.setEnabled(self.current_tab_info.copy)
        self.ui.actionCut.setEnabled(self.current_tab_info.cut)
        self.ui.actionDelete_2.setEnabled(self.current_tab_info.delete_selection)

    def selection_enable(self, e):
        self.current_tab_info.copy = e
        self.current_tab_info.cut = e
        self.current_tab_info.delete_selection = e

    def copy(self):
        self.current_plain_text_widget.copy()
    def paste(self):
        self.current_plain_text_widget.paste()
    def delete_2(self):
        self.current_plain_text_widget.textCursor().removeSelectedText()

    def cut(self):
        self.current_plain_text_widget.cut()

    def insert_date_today(self):
        text: str = self.current_plain_text_widget.toPlainText()
        new_text :str = "%s%s" %(text,System_info.time_now)
        self.current_plain_text_widget.setPlainText(new_text)
        cursor = self.current_plain_text_widget.textCursor()
        cursor.movePosition(QTextCursor.End) # or you can put 11 check in https://doc.qt.io/qt-6/qtextcursor.html
        self.current_plain_text_widget.setTextCursor(cursor)

    def undo_available(self,e):
        self.ui.actionUndo.setEnabled(e)

    def is_undo_available(self):
        value = self.current_plain_text_widget.document().isUndoAvailable()
        self.ui.actionUndo.setEnabled(value)

    def undo(self):
        self.current_plain_text_widget.undo()


    def redo(self):
        print("redooo")
        self.current_plain_text_widget.redo()

    def redo_available(self,e):
        print(e)
        self.ui.actionRedo.setEnabled(e)

    def display_about_window(self):
        dialog = QDialog()
        win = Ui_Dialog()
        win.display_dialog()


class WindowsInfo(QMessageBox):

    def __init__(self, title: str, message: str, icon_type: str| int, error_number: str | int = None):
        """
        This Class will display to create info, warining and error dialog windows
        :param title : The title of the Dialog Window
        :param message : The message inside the dialog Window
        :param icon: The main icon on the dialog window
        :param error_number: If an error number exist place the number if not by default it is None, place the string or the number code

        -----+ Icon str| int : Error code  [ERROR or 0], Warining code: [WARINING or 1] , Information code : [INFORMATION or INFOR or 2]

        """
        super().__init__()

        if isinstance(icon_type, int): # Transfor the integer into string to be used
            icon_type = str(icon_type)

        self.diag_win_title: str = title
        self.diag_text_icon_type: str = icon_type
        self.diag_message: str = message
        self.error_number: str|int = error_number

        self.setWindowTitle(self.diag_win_title)
        self.define_dialog_icon()
        self.set_message(self.diag_message)

    def define_dialog_icon(self):

        if self.diag_text_icon_type.isdigit():

            match int(self.diag_text_icon_type):
                case 0:
                    self.setIcon(QMessageBox.Critical)
                case 1:
                    self.setIcon(QMessageBox.Warning)
                case 2:
                    self.setIcon(QMessageBox.Information)
        else:
            match self.diag_text_icon_type:
                case "ERROR":
                    self.setIcon(QMessageBox.Critical)
                case "WARNING":
                    self.setIcon(QMessageBox.Warning)
                case "INFORMATION":
                    self.setIcon(QMessageBox.Information)
                case "INFO":
                    self.setIcon(QMessageBox.Information)

    def set_message(self, message:str):

        """
        Modify the message on the dialaog box
        :param message: the message you want to transmit
        :return:
        """

        for icon_type in ["ERROR","0"]:
            if self.diag_text_icon_type == icon_type:

                if self.error_number == None:
                    self.error_number = ""

                self.setText(f"Erro {self.error_number}: {message}")

        for icon_type in ["INFORMATION","INFO", "2"]:
            if self.diag_text_icon_type == icon_type:
                self.setText(f"Info: {message}")

        for icon_type in ["WARNING","1"]:
            if self.diag_text_icon_type == icon_type:
                self.setText(f"Warning: {message}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowApp()
    window.show()
    exitCode = app.exec()
    sys.exit(exitCode)  # After this line it won't print anything due to sys.exit(), exit of the program
