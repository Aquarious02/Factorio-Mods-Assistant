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

        self.mods_in_table = {}

        self.mods_handler = ModsHandler()
        self.searcher = Searcher(self)

        #
        # menu
        #
        self.ui.action_open.triggered.connect(self.open)
        self.ui.action_save.triggered.connect(self.save)
        self.ui.action_save_as.triggered.connect(self.save_as)
        self.ui.action_make_copy.triggered.connect(self.make_copy)

        self.ui.checkBox_choose_all.clicked.connect(self.choose_all)
        self.ui.checkBox_enable.clicked.connect(self.change_state)

    def update_table(self, from_open: bool = True):
        """
        Updates table with mods
        :param from_open: recreates mods (don't take into account previous state)
        """
        self.ui.tableWidget.setRowCount(len(self.mods_in_table))
        for mode_index, mode in enumerate(self.mods_in_table.items()):
            name, state = mode

            # If item doesn't exist
            item_from_table = self.ui.tableWidget.item(mode_index, 0)
            if item_from_table is None:
                mode_item = QtWidgets.QTableWidgetItem()
                mode_item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignVCenter)

                if name == 'base':
                    mode_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled)
            else:
                mode_item = item_from_table

            mode_item.setText(name)

            self.ui.tableWidget.setRowHidden(mode_index, False)  # Because of searcher hiding

            if from_open:
                if state:
                    mode_item.setCheckState(QtCore.Qt.Checked)
                else:
                    mode_item.setCheckState(QtCore.Qt.Unchecked)
            else:
                if state or mode_item.checkState():
                    mode_item.setCheckState(QtCore.Qt.Checked)
                else:
                    mode_item.setCheckState(QtCore.Qt.Unchecked)

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


class Searcher:
    """
    More information here: https://www.learnpyqt.com/courses/adanced-ui-features/widget-search-bar/
    """
    def __init__(self, MainGUI):
        """
        :param MainGUI: GUI instance to operate
        """
        self.outer_GUI = MainGUI

        #
        # Objects connecting
        #
        self.search_line_edit = self.outer_GUI.ui.lineEdit_search
        self.search_counter = self.outer_GUI.ui.label_search_counter
        self.match_case_button = self.outer_GUI.ui.pushButton_match_case
        self.completer = QtWidgets.QCompleter(self.mods_names)

        self.to_match_case = False
        self.result_index = 0
        self.match_case()  # to set CaseSensivity

        #
        # Actions Connecting
        #
        self.match_case_button.clicked.connect(self.match_case)
        self.search_line_edit.textChanged.connect(self.search)
        self.search_line_edit.setCompleter(self.completer)

    def search(self):
        """
        Main node of Searcher.
        """
        search_pattern = self.search_line_edit.text()
        self.outer_GUI.update_table(from_open=False)
        if search_pattern != '':
            if not self.to_match_case:
                search_pattern = search_pattern.lower()

            hidden_mods = len(self.outer_GUI.mods_in_table.keys())

            for mod_index, mod_name in enumerate(self.outer_GUI.mods_in_table.keys()):
                if not self.to_match_case:
                    mod_name = mod_name.lower()

                if search_pattern not in mod_name:
                    self.outer_GUI.ui.tableWidget.setRowHidden(mod_index, True)
                    hidden_mods -= 1
                    self.search_counter.setText(str(hidden_mods))

        else:
            self.reset()

    def match_case(self):
        """
        Changes match_case parameter if pushButton was pressed
        """
        if self.match_case_button.isChecked():
            self.to_match_case = True
            self.completer.setCaseSensitivity(QtCore.Qt.CaseSensitive)
        else:
            self.to_match_case = False
            self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.search()

    @property
    def mods_names(self):
        """
        Collect names of mods
        :return:
        """
        return self.outer_GUI.mods_handler.mods.keys()

    def update_completer(self):
        """
        Updated completer if mods were changed
        :return:
        """
        self.search_line_edit.setCompleter(None)
        self.completer = QtWidgets.QCompleter(list(set(self.mods_names)))
        self.match_case()  # to set CaseSensivity
        self.search_line_edit.setCompleter(self.completer)

    def reset(self):
        """
        Resets state of searcher widget
        """
        self.search_counter.setText('')


def excepthook(exc_type, exc_value, exc_tb):
    """
    For catching errors in PyQt
    """
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(tb)
    QtWidgets.QApplication.quit()


if __name__ == '__main__':
    MainWindow.start()
