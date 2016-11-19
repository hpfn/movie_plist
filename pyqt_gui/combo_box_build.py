from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QMessageBox
# from PyQt5.QtCore import QEvent
from info_in_db.movie_plist_sqlite3 import DataStorage

from .combo_box_interact import InteractBox


class Combo(QComboBox):
    def __init__(self, will_do, update_object=None, seen_object=None, scanlocal_htmlf=None, browser_obj=None):
        super().__init__()
        self.to_do = will_do
        self.path_html = scanlocal_htmlf
        self.watch_again = seen_object
        self.watch_again_list = None
        self.up_date = update_object
        self.insert_movie_file_list = None
        self.browser_reload = browser_obj
        self.stored_data = DataStorage()
        self.movies_stored = ""

        self.combo_list()

    def combo_list(self):
        def update():
            self.addItem("insert movie file ")
            self.insert_movie_file_list = ['insert movie file']
            self.movies_stored = self.stored_data.no_movie_yet()
            # doing this here make update in confirm_option
            # method easier to read
            for i in self.movies_stored:
                self.insert_movie_file_list.append(i[0])

        def remove():
            self.addItem("remove movie from db")
            self.movies_stored = self.stored_data.movie_title_list()

        def seen():
            self.addItem("seen movies")
            self.watch_again_list = ['seen movies']
            self.movies_stored = self.stored_data.movie_seen()
            # doing this here make remove() in confirm_option
            # method easier to read
            for i in self.movies_stored:
                self.watch_again_list.append(i[0])

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
        self.activated.connect(lambda s_item: self.confirm_option(s_item, self.currentText()))

    def confirm_option(self, index, movie_selected):
        """ show msg about what to_do with the movie selected"""
        txt_info = "You will " + self.to_do + " " + movie_selected
        msg = QMessageBox()
        reply = msg.question(self, 'The selected movie', txt_info,
                             QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)

        if reply == QMessageBox.Yes:
            msg.setText('remove this window!!!')

            def update():
                update_list_html = InteractBox(movie_selected)
                update_list_html.insert_movie_file_action(self.path_html, self.browser_reload)
                self.removeItem(index)

            def remove():
                remove_item = InteractBox(movie_selected)
                remove_item.movie_remove(self.up_date, self.watch_again)
                self.removeItem(index)

            def seen():
                watch_movie = InteractBox(movie_selected)
                watch_movie.watch_movie()

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





















































