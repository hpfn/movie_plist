from PyQt5.QtWidgets import QComboBox
from info_in_db.movie_plist_sqlite3 import DataStorage


class Combo(QComboBox):
    def __init__(self):
        super().__init__()
        self.stored_data = DataStorage()
        self.movies_stored = []

        self.combo_list()

    def combo_list(self):
        """
            sqlite returns a list of tuples
            using a for loop to have a 'str' item
            and be easier to find the index on
            confirm_option method (InteractBox())
        """
        pass
        # self.show_list()

    def show_list(self):
        for title_year in self.movies_stored:
            self.add_to_cbox(title_year)

    def add_to_cbox(self, item):
        self.addItem(item)

    def get_item_selected(self):
        self.activated.connect(lambda s_item: self.confirm_option(s_item, self.currentText()))

    def confirm_option(self, index, movie_selected):
        """ show msg about what to_do with the movie selected"""
        pass





















































