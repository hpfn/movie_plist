from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QEvent
from info_in_db.movie_plist_sqlite3 import DataStorage

from subprocess import call


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

        def seen():
            self.addItem("seen movies")

        option = {"update": update,
                  "remove": remove,
                  "watch_again": seen}
        option[self.to_do]()

    def combo_list(self):
        def update():
            self.movies_stored = self.stored_data.no_movie_yet()

        def remove():
            self.movies_stored = self.stored_data.movie_title_list()

        def seen():
            self.movies_stored = self.stored_data.movie_seen()

        option = {"update": update,
                  "remove": remove,
                  "watch_again": seen}

        option[self.to_do]()
        self.show_list()

    def show_list(self):
        for title_year in self.movies_stored:
            title_l = list(title_year)
            self.add_to_cbox(title_l[0])

    def add_to_cbox(self, item):
        self.addItem(item)

    def get_item_selected(self):
        self.activated.connect(lambda s_item: self.confirm_option(self.currentText()))

    def confirm_option(self, movie_selected):
        """ show msg about what to_do with the movie selected"""
        txt_info = "You will " + self.to_do + " " + movie_selected
        msg = QMessageBox()
        reply = msg.question(self, 'The selected movie', txt_info,
                             QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)

        if reply == QMessageBox.Yes:
            # call db
            # rebuild .html file
            msg.setText('remove this window!!!')
            def update():
                print(movie_selected)

            def remove():
                print(movie_selected)

            def seen():
                path = self.stored_data.movie_to_watchagain(movie_selected)
                to_watch = str(path[0]) + '/' + str(path[1])
                call(['/usr/bin/vlc', to_watch])

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
