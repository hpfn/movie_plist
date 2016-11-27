from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QMessageBox
# from PyQt5.QtCore import QEvent
from info_in_db.movie_plist_sqlite3 import DataStorage

from .combo_box_interact import InteractBox


class Combo(QComboBox):
    def __init__(self, will_do, update_object=None, seen_object=None, browser_obj=None):
        super().__init__()
        self.to_do = will_do
        self.watch_again = seen_object
        self.up_date = update_object
        self.browser_reload = browser_obj
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
        def update():
            self.movies_stored = ['insert movie file']
            for i in self.stored_data.no_movie_yet():
                self.movies_stored.append(i[0])

        def remove():
            self.movies_stored = ['remove movie from db']
            for i in self.stored_data.movie_title_list():
                self.movies_stored.append(i[0])

        def seen():
            self.movies_stored = ['seen movies']
            for i in self.stored_data.movie_seen():
                self.movies_stored.append(i[0])

        option = {"update": update,
                  "remove": remove,
                  "watch_again": seen}

        option[self.to_do]()
        self.show_list()

    def show_list(self):
        for title_year in self.movies_stored:
            self.add_to_cbox(title_year)

    def add_to_cbox(self, item):
        self.addItem(item)

    def get_item_selected(self):
        self.activated.connect(lambda s_item: self.confirm_option(s_item, self.currentText()))

    def confirm_option(self, index, movie_selected):
        """ show msg about what to_do with the movie selected"""
        txt_info = "You will " + self.to_do + " " + movie_selected
        msg = QMessageBox()
        reply = msg.question(self, 'The selected movie', txt_info,
                             QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)

        if reply == QMessageBox.Yes:
            msg.setText('remove this window!!!')

            html_cboxlist_changes = InteractBox(movie_selected)

            def update():
                html_cboxlist_changes.insert_movie_file_action(self.browser_reload)
                self.removeItem(index)

            def remove():
                html_cboxlist_changes.movie_remove(self.up_date, self.watch_again, self.browser_reload)
                self.removeItem(index)

            def seen():
                html_cboxlist_changes.watch_movie()

            option = {"update": update,
                      "remove": remove,
                      "watch_again": seen}

            option[self.to_do]()
        else:
            # how to ignore this ???
            # QEvent.setAccepted()
            msg.setText('Doing nothing.')

        msg.show()
        msg.exec_()





















































