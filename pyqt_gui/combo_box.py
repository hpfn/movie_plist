from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QEvent
from info_in_db.movie_plist_sqlite3 import DataStorage

from subprocess import call

from data.pyscan import PyScan
import html_file.create_page


class Combo(QComboBox):
    def __init__(self, will_do, scan_local=None, browser_obj=None):
        super().__init__()
        self.to_do = will_do
        self.scan_local = scan_local
        self.browser_reload = browser_obj
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
        self.activated.connect(lambda s_item: self.confirm_option(s_item, self.currentText()))

    def confirm_option(self, index, movie_selected):
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
                p_file = self.stored_data.movie_path(movie_selected)
                # scan selected movie dir
                scan_dir = PyScan(p_file[0])
                scan_dir = scan_dir.dir_to_scan()
                # file name
                file_n = scan_dir[0][2]
                self.stored_data.update_movie_file(file_n,movie_selected)
                # update list
                self.removeItem(index)
                # edit .html file ? re-create by now. First get the movies
                # then rm the html file and re-create.
                # This can be better
                unseen_movies = self.stored_data.unseen_movie()
                html_f = self.scan_local + '/' + 'pymovieinfo.html'
                call(['/bin/rm', html_f])
                html_file.create_page.generate_html(self.scan_local, unseen_movies)
                self.browser_reload.reload()

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
