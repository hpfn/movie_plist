from PyQt5.QtWidgets import QComboBox
from info_in_db.movie_plist_sqlite3 import DataStorage


class Combo(QComboBox):
    def __init__(self, will_do):
        super().__init__()
        self.to_do = will_do
        self.stored_data = DataStorage()
        self.movies_stored = ""

        self.first_item_combo()
        self.combo_list()

    def first_item_combo(self):
        def update():
            self.addItem("insert movie file ")

        def remove():
            self.addItem("remove movie from hd")

        option = {"update": update,
                  "remove": remove}
        option[self.to_do]()

    def combo_list(self):
        def update():
            self.movies_stored = self.stored_data.no_movie_yet()

        def remove():
            self.movies_stored = self.stored_data.movie_list_title()

        option = {"update": update,
                  "remove": remove}

        option[self.to_do]()
        self.show_list()

    def show_list(self):
        for title_year in self.movies_stored:
            title_l = list(title_year)
            self.add_to_cbox(title_l[0])

    def add_to_cbox(self, item):
        self.addItem(item)
