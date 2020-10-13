from PyQt5 import QtCore, QtWidgets
import traceback
import sys

from GUI_schemas.Scheme import Ui_MainWindow
from Mods_assistant_lib import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.mods_handler = ModsHandler()

        self.mods_in_table = []

        #
        # menu
        #
        self.ui.action_open.triggered.connect(self.open)
        self.ui.action_save.triggered.connect(self.save)
        self.ui.action_save_as.triggered.connect(self.save_as)
        self.ui.action_make_copy.triggered.connect(self.make_copy)

    def update_table(self):
        self.ui.tableWidget.setRowCount(len(self.mods_in_table))
        for mode_index, mode in enumerate(self.mods_in_table):
            mode_name_item = QtWidgets.QTableWidgetItem()
            mode_name_item.setText(mode['name'])
            mode_name_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.tableWidget.setItem(mode_index, 0, mode_name_item)

            mode_state_item = QtWidgets.QTableWidgetItem()
            if mode['enabled']:
                mode_state_item.setCheckState(QtCore.Qt.Checked)
            else:
                mode_state_item.setCheckState(QtCore.Qt.Unchecked)

            self.ui.tableWidget.setItem(mode_index, 1, mode_state_item)

    def open(self):
        """
        Open mods file
        """
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, directory=self.mods_handler.mods_path or 'mods')[0]
        # file_name = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        if file_name != '':
            self.mods_handler.mods_file_path = file_name  # it was "empty" because of initialization above
            self.mods_in_table = self.mods_handler.open_json()
            self.update_table()

    def save(self):
        pass

    def save_as(self):
        pass

    def make_copy(self):
        pass


    @classmethod
    def start(cls):
        sys.excepthook = excepthook

        app = QtWidgets.QApplication([])
        application = cls()
        application.show()

        sys.exit(app.exec())


def excepthook(exc_type, exc_value, exc_tb):
    """
    For catching errors in PyQt
    """
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(tb)
    QtWidgets.QApplication.quit()


if __name__ == '__main__':
    MainWindow.start()
