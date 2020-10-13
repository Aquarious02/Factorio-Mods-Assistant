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

        self.mods_in_table = {}

        #
        # menu
        #
        self.ui.action_open.triggered.connect(self.open)
        self.ui.action_save.triggered.connect(self.save)
        self.ui.action_save_as.triggered.connect(self.save_as)
        self.ui.action_make_copy.triggered.connect(self.make_copy)

        self.ui.checkBox_choose_all.clicked.connect(self.choose_all)
        self.ui.checkBox_enable.clicked.connect(self.change_state)

    def update_table(self):
        self.ui.tableWidget.setRowCount(len(self.mods_in_table))
        for mode_index, mode in enumerate(self.mods_in_table.items()):
            name, state = mode
            mode_item = QtWidgets.QTableWidgetItem()
            mode_item.setText(name)
            # mode_name_item.setTextAlignment(QtCore.Qt.AlignCenter)
            mode_item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)

            if state:
                mode_item.setCheckState(QtCore.Qt.Checked)
            else:
                mode_item.setCheckState(QtCore.Qt.Unchecked)

            # if mode['name'] == 'base':
            #     mode_item.setVisible(False)

            self.ui.tableWidget.setItem(mode_index, 0, mode_item)

    def update_changes(self):
        """Writes mods from table to mods_handler"""
        for row in range(self.ui.tableWidget.rowCount()):
            item = self.ui.tableWidget.item(row, 0)
            self.mods_handler.mods[item.text()] = item.checkState() == 2

    def choose_all(self):
        """
        Select all items in table
        """
        if self.sender().isChecked():
            self.ui.tableWidget.selectAll()
        else:
            self.ui.tableWidget.clearSelection()
        self.ui.tableWidget.setFocus()

        # for row in range(self.ui.tableWidget.rowCount()):
        #     self.ui.tableWidget.setItemSelected(self.ui.tableWidget.item(row, 0), True)

    def change_state(self):
        """
        Change state of selected items
        """
        items = self.ui.tableWidget.selectedItems()

        new_state = self.sender().isChecked()
        for item in items:
            if new_state:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)

        self.ui.tableWidget.setFocus()

    def open(self):
        """
        Open mods file
        """
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, directory=self.mods_handler.mods_path or 'mods')[0]
        if file_name != '':
            self.mods_handler.mods_file_path = file_name  # it was "empty" because of initialization above
            self.mods_handler.update_mods()
            self.mods_in_table = self.mods_handler.mods
            self.update_table()

    def save(self):
        self.update_changes()
        if self.mods_handler.mods_file_path is None:
            self.save_as()
        else:
            self.mods_handler.save_mods()

    def save_as(self):
        """
        Opens fileDialog to ask where to save
        """
        self.update_changes()
        file_path = QtWidgets.QFileDialog.getSaveFileName(self, directory=self.mods_handler.mods_path or 'mods')[0]
        if file_path != '':
            self.mods_handler.save_mods(file_path=file_path)

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
